import math
from simulation.raid import RaidSimulation

class Raid5Simulation(RaidSimulation):

    def __init__(self, drives):
        """
        Initialize the RAID 5 simulation.
        
        :param drives: List of drive sizes in bytes.
        :param block_size: Size of each block for striping (in bytes).
        """
        super().__init__(drives)
        self.blocks = len(drives)
        self.block_size = math.ceil(min(len(drive) for drive in self.drives) / self.blocks)

    def write(self, data):
        
        if isinstance(data, str):
            data = data.encode() 

        total_data_length = len(data)

        if total_data_length > self.space_in_raid():
            raise ValueError("Not enough space in the RAID to write the data.")

        current_block = 0
        
        for i in range(total_data_length):
        
            block_data = data[i]
            drive_index = i % (self.num_drives - 1)
            position = i // (self.num_drives - 1)

            parity_drive = self.num_drives - 1 - current_block
            real_drive = drive_index if drive_index < parity_drive else drive_index + 1

            self.drives[real_drive][position] = block_data
            
            parity_data = 0b0
            for index in range(self.num_drives):
                if index != parity_drive:
                    parity_data ^= self.drives[index][position]

            if drive_index == self.num_drives - 2 or total_data_length - i == 1:
                self.drives[parity_drive][position] = parity_data

                if (position + 1) % self.block_size == 0:
                    current_block += 1

        self.used_space += total_data_length
        

    def read(self):
        
        data = bytearray()
        current_block = 0
        
        for i in range(self.used_space):
            drive_index = i % (self.num_drives - 1)
            position = i // (self.num_drives - 1)
            
            parity_drive = self.num_drives - 1 - current_block
            real_drive = drive_index if drive_index < parity_drive else drive_index + 1
            
            if self.drives[real_drive] == None:
                data.append(0b0)
            else:
                data.append(self.drives[real_drive][position])
            
            if drive_index == self.num_drives - 2 and (position + 1) % self.block_size == 0:
                current_block += 1

        # print(data)
        
        return data.decode()

    def simulate_output(self):
        """
        Return a string representation of the simulated drives (showing the mirrored view with parity).
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
        return sum(len(drive) for drive in self.drives) - min(len(drive) for drive in self.drives)


    def size_in_use(self):
        return self.used_space
        

    def space_in_raid(self):
        return self.total_size() - self.size_in_use()

    def recovery(self):
        """
        Simulate the recovery process for a failed drive in the RAID 5 array.
        This will reconstruct the missing data based on the parity.
        """
        failed_drive = None
        for i in range(self.num_drives):
            if self.drives[i] is None:
                failed_drive = i
                break

        if failed_drive is None:
            raise ValueError("No failed drive detected.")
        
        working_drive = []
        for i in range(self.num_drives):
            if i != failed_drive and self.drives[i] is not None:
                working_drive.append(self.drives[i])
        
        if len(working_drive) == 0:
            raise ValueError("No healthy drive available for recovery.")

        drive_size = len(working_drive[0])
        self.drives[failed_drive] = bytearray(drive_size)

        for i in range(drive_size):

            recover_data = 0b0
            for drive in working_drive:
                
                recover_data ^= drive[i]
                # print(f"XOR {drive[i]} {chr(drive[i])} RecoverData: {recover_data} {chr(recover_data)}")

            self.drives[failed_drive][i] = recover_data

            # print("-----")