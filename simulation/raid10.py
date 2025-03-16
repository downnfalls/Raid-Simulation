import math
from simulation.raid import RaidSimulation

class Raid10Simulation(RaidSimulation):
    def __init__(self, drives, block_size=1):
        
        if len(drives) % 2 != 0:
            raise ValueError("RAID 10 requires an even number of drives for mirroring.")
        
        super().__init__(drives)
        self.block_size = block_size
        self.num_mirrored_pairs = len(drives) // 2

    def write(self, data):
        
        if isinstance(data, str):
            data = data.encode()

        total_data_length = len(data)
        if total_data_length > self.total_size():
            raise ValueError("Not enough space in the RAID to write the data.")

        blocks_needed = math.ceil(total_data_length / self.block_size)
        current_block = 0

        for i in range(blocks_needed):
            start_idx = i * self.block_size
            end_idx = start_idx + self.block_size
            block_data = data[start_idx:end_idx]

            primary_drive = current_block % self.num_mirrored_pairs
            mirror_drive = primary_drive + self.num_mirrored_pairs

            start_position = (current_block // self.num_mirrored_pairs) * self.block_size
            end_position = start_position + len(block_data)

            self.drives[primary_drive][start_position:end_position] = block_data
            self.drives[mirror_drive][start_position:end_position] = block_data  # Mirroring the data

            current_block += 1

        self.used_space += total_data_length

    def read(self):
        
        result = bytearray()
        total_blocks = math.ceil(self.used_space / self.block_size)

        for i in range(total_blocks):
            start_position = i * self.block_size
            block_data = bytearray()

            for j in range(self.num_mirrored_pairs):
                drive = self.drives[j]  # Read from primary drives only
                if (drive != None):
                    block_data.extend(drive[start_position:start_position + self.block_size])

            result.extend(block_data)

        return (bytes(result)).decode()

    def simulate_output(self):
        
        return "\n".join(
            f"Drive #{str(drive+1)}:\n " + ("\n Failed" if self.drives[drive] == None else "\n ".join(
                "  ".join(f"{str(byte).rjust(3, '0')}({' ' if byte == 0 else chr(byte)})".ljust(6) for byte in self.drives[drive][i:i + 8])
                for i in range(0, len(self.drives[drive]), 8)
            ))
            for drive in range(self.num_mirrored_pairs * 2)
        )

    def total_size(self):
        
        return sum(len(drive) for drive in self.drives[:self.num_mirrored_pairs])

    def size_in_use(self):
        
        return self.used_space

    def space_in_raid(self):
        
        return self.total_size() - self.size_in_use()
    
    def recovery(self):
       
        failed_drives = []
        for i in range(self.num_drives):
            if self.drives[i] is None:
                failed_drives.append(i)

        if len(failed_drives) == 0:
            raise ValueError("No failed drive detected.")

        if not isinstance(failed_drives, list):
            raise ValueError("Failed drives must be provided as a list.")
        
        # Rebuild the data for the failed drives.
        for drive in failed_drives:
            # Identify the mirrored pair.
            mirror_drive = drive + self.num_mirrored_pairs if drive < self.num_mirrored_pairs else drive - self.num_mirrored_pairs
            
            # If the failed drive is in the first half (primary), recover from the mirror (secondary).
            if drive < self.num_mirrored_pairs:
                if self.drives[mirror_drive] is not None:
                    # Copy data from the mirror drive.
                    self.drives[drive] = self.drives[mirror_drive].copy()
                else:
                    raise ValueError(f"Both drives in the mirrored pair for drive {drive} are failed. Recovery cannot proceed.")
            
            # If the failed drive is in the second half (secondary), recover from the primary.
            else:
                if self.drives[mirror_drive] is not None:
                    # Copy data from the primary drive.
                    self.drives[drive] = self.drives[mirror_drive].copy()
                else:
                    raise ValueError(f"Both drives in the mirrored pair for drive {drive} are failed. Recovery cannot proceed.")
        
