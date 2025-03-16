import math
from simulation.raid import RaidSimulation

class Raid0Simulation(RaidSimulation):

    def __init__(self, drives, block_size=1):
        """
        Initialize the RAID 0 simulation.
        
        :param drives: List of drive sizes in bytes.
        :param block_size: Size of each block for striping (in bytes).
        """
        super().__init__(drives)
        self.block_size = block_size

    def write(self, data):
        
        """
        Simulate writing data to the RAID 0 array by striping across the drives.
        
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

        # Iterate through the blocks and stripe them across the drives
        for i in range(blocks_needed):
            start_idx = i * self.block_size
            end_idx = start_idx + self.block_size
            block_data = data[start_idx:end_idx]

            # Determine which drive to write this block to based on the current block index
            drive_index = current_block % self.num_drives

            # Calculate where to write the data on the selected drive (using contiguous blocks)
            start_position = (current_block // self.num_drives) * self.block_size
            end_position = start_position + len(block_data)

            # Write the block to the drive at the correct position
            drive_size = len(self.drives[drive_index])
            if end_position > drive_size:
                end_position = drive_size  # Ensure we don't go past the end of the drive
                
            self.drives[drive_index][start_position:end_position] = block_data

            current_block += 1

        # Update the used space after writing
        self.used_space += total_data_length

    def read(self):
        """
        Simulate reading the RAID 0 data from the drives by reassembling the blocks.
        
        :return: The read data as bytes.
        """
        result = bytearray()
        total_blocks = math.ceil(self.used_space / self.block_size)

        # Reassemble the blocks in the correct order
        for i in range(total_blocks):
            start_position = i * self.block_size
            block_data = bytearray()

            # Read the data from each drive based on the block index
            for j in range(self.num_drives):
                drive = self.drives[j]
                block_data.extend(drive[start_position:start_position + self.block_size])

            result.extend(block_data)

        return (bytes(result)).decode()

    def simulate_output(self):
        """
        Return a string representation of the simulated drives.
        """
        return "\n".join(
            f"Drive #{str(drive+1)}:\n "
            + ("\n Failed" if self.drives[drive] == None else "\n ".join(
                "  ".join(f"{str(byte).rjust(3, '0')}({' ' if byte == 0 else chr(byte)})".ljust(6) for byte in self.drives[drive][i:i + 8])
                for i in range(0, len(self.drives[drive]), 8)
            ))
            for drive in range(self.num_drives)
        )
    
    def total_size(self):
        """
        Calculate the total size of the RAID 0 setup (sum of all drive sizes).
        """
        return sum(len(drive) for drive in self.drives)

    def size_in_use(self):
        """
        Return the total amount of used space in the RAID 0 setup.
        :return: The used space in bytes.
        """
        return self.used_space

    def space_in_raid(self):
        """
        Return the available space in the RAID 0 setup.
        :return: The available space in bytes.
        """

        return self.total_size() - self.size_in_use()
    
    def recovery(self):
        raise ValueError("Raid 0 cannot recovery data")
