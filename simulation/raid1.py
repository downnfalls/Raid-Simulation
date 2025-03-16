import math
from simulation.raid import RaidSimulation

class Raid1Simulation(RaidSimulation):

    def __init__(self, drives, block_size=1):
        """
        Initialize the RAID 1 simulation.
        
        :param drives: List of drive sizes in bytes.
        :param block_size: Size of each block for striping (in bytes).
        """
        super().__init__(drives)
        self.block_size = block_size

        # Find the size of the smallest drive (to determine the usable capacity)
        self.smallest_drive_size = min(len(drive) for drive in self.drives)

    def write(self, data):
        """
        Simulate writing data to the RAID 1 array by mirroring across all drives.
        
        :param data: Data to write (string or bytes).
        :raises ValueError: If there is not enough space to write the data.
        """
        if isinstance(data, str):
            data = data.encode()  # Convert string to bytes
            
        total_data_length = len(data)
        
        # Check if there is enough space in the RAID before writing
        if total_data_length > self.total_size():
            raise ValueError("Not enough space in the RAID to write the data.")

        blocks_needed = math.ceil(total_data_length / self.block_size)

        current_block = 0

        # Iterate through the blocks and mirror them across all drives
        for i in range(blocks_needed):
            start_idx = i * self.block_size
            end_idx = start_idx + self.block_size
            block_data = data[start_idx:end_idx]

            # Write the block to all drives, respecting the smallest drive size
            for drive_index in range(self.num_drives):
                # Ensure the block does not exceed the smallest drive size
                drive_size = len(self.drives[drive_index])
                if current_block * self.block_size < drive_size:
                    # Calculate where to write the data on the selected drive (using contiguous blocks)
                    start_position = current_block * self.block_size
                    end_position = start_position + len(block_data)

                    # Ensure we do not go beyond the drive's size
                    if end_position > drive_size:
                        end_position = drive_size
                    
                    # Write the block to the drive at the correct position
                    self.drives[drive_index][start_position:end_position] = block_data

            current_block += 1

        # Update the used space after writing
        self.used_space += total_data_length

    def read(self):
        """
        Simulate reading the RAID 1 data from any of the drives (they are identical).
        
        :return: The read data as bytes.
        """
        result = bytearray()
        total_blocks = math.ceil(self.smallest_drive_size / self.block_size)

        # Reassemble the blocks in the correct order (we can read from any drive)
        for i in range(total_blocks):
            start_position = i * self.block_size
            block_data = bytearray()

            # Read data from the first drive (as all drives are identical)
            drive = self.drives[0]  # Just read from the first drive, others are identical
            block_data.extend(drive[start_position:start_position + self.block_size])

            result.extend(block_data)

        return (bytes(result)).decode()

    def simulate_output(self):
        """
        Return a string representation of the simulated drives (mirror view of the drives).
        """
        return "\n".join(
            f"Drive #{str(drive)}:\n "
            + ("\n Failed" if self.drives[drive] == None else "\n ".join(
                "  ".join(f"{str(byte).rjust(3, '0')}({' ' if byte == 0 else chr(byte)})".ljust(6) for byte in self.drives[drive][i:i + 8])
                for i in range(0, len(self.drives[drive]), 8)
            ))
            for drive in range(self.num_drives)
        )
    
    def total_size(self):
        # The total size is the size of the smallest drive, as all drives are mirrored
        return self.smallest_drive_size

    def size_in_use(self):
        """
        Calculate the total used space in the RAID, considering that data is mirrored across all drives.
        :return: The total used space in bytes.
        """
        # The used space is tracked by the self.used_space variable
        return self.used_space

    def space_in_raid(self):
        """
        Calculate the available space in the RAID.
        :return: The available space in bytes.
        """
        # Available space is the total size of the smallest drive minus the used space
        return self.total_size() - self.size_in_use()

    def recovery(self):
        """
        Simulate recovering a failed drive in the RAID 1 array.
        
        :param failed_drive_index: The index of the drive that needs to be recovered.
        :raises ValueError: If the drive index is invalid or no healthy drive is available.
        """
        failed_drive = None
        for i in range(self.num_drives):
            if self.drives[i] is None:
                failed_drive = i
                break

        if failed_drive is None:
            raise ValueError("No failed drive detected.")

        # Find a working drive
        working_drive = None
        for i in range(self.num_drives):
            if i != failed_drive and self.drives[i] is not None:
                working_drive = self.drives[i]
                break
        
        if working_drive is None:
            raise ValueError("No healthy drive available for recovery.")

        # Recover the failed drive by copying data from a working drive
        self.drives[failed_drive] = working_drive.copy()