from abc import ABC, abstractmethod
import array

class RaidSimulation(ABC):

    def __init__(self, drives):
        """
        Initialize the RAID simulation with the list of drives.
        
        :param drives: List of drive sizes in bytes.
        """
        self.drives = [bytearray(size) for size in drives]
        self.num_drives = len(drives)
        self.drives_array = drives

        self.used_space = 0

    @abstractmethod
    def total_size(self):
        """Return the total size of the RAID array."""
        pass

    @abstractmethod
    def size_in_use(self):
        """Return the size of data currently stored in the RAID array."""
        pass

    @abstractmethod
    def space_in_raid(self):
        """Return the remaining space available in the RAID array."""
        pass

    @abstractmethod
    def simulate_output(self):
        """Return a string representation of the RAID array's state."""
        pass

    @abstractmethod
    def read(self):
        """Simulate reading data from the RAID array."""
        pass

    @abstractmethod
    def write(self, data):
        """Simulate writing data to the RAID array."""
        pass

    def destroy(self, drive):

        self.drives[drive] = None

    def clear(self):

        self.drives = [bytearray(len(drive)) for drive in self.drives]
        self.used_space = 0

    @abstractmethod
    def recovery(self):
        pass
