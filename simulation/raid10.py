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

            # Updated logic for pairing: 0-1, 2-3, 4-5
            pair_index = (current_block % self.num_mirrored_pairs) * 2
            primary_drive = pair_index
            mirror_drive = pair_index + 1

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
        output = []
        for i in range(0, self.num_drives, 2):
            output.append(f"Mirror: Drive #{i + 1} <-> Drive #{i + 2}:\n")

            # Print Primary Drive
            if self.drives[i] is None:
                output.append(f" Primary Drive #{i + 1}: FAILED\n")
            else:
                output.append(f" Primary Drive #{i + 1}:\n")
                output.append(self.format_drive_output(self.drives[i]))

            # Print Mirror Drive
            if self.drives[i + 1] is None:
                output.append(f" Mirror Drive #{i + 2}: FAILED\n")
            else:
                output.append(f" Mirror Drive #{i + 2}:\n")
                output.append(self.format_drive_output(self.drives[i + 1]))

            output.append("\n")

        return ''.join(output)


    def format_drive_output(self, drive):
        return "\n".join(
            "  " + "  ".join(f"{str(byte).rjust(3, '0')}({' ' if byte == 0 else chr(byte)})".ljust(6) for byte in drive[i:i + 8])
            for i in range(0, len(drive), 8)
        ) + "\n"


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

        for drive in failed_drives:
            # Pair logic: if even, mirror is +1; if odd, mirror is -1
            if drive % 2 == 0:
                mirror_drive = drive + 1
            else:
                mirror_drive = drive - 1

            if self.drives[mirror_drive] is not None:
                self.drives[drive] = self.drives[mirror_drive].copy()
            else:
                raise ValueError(f"Both drives in the mirrored pair for drive {drive} are failed. Recovery cannot proceed.")

        
