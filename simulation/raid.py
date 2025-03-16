from abc import ABC, abstractmethod

class RaidSimulation(ABC):

    def __init__(self, drives):
        self.drives = [bytearray(size) for size in drives]
        self.num_drives = len(drives)
        self.drives_array = drives

        self.used_space = 0

    @abstractmethod
    def total_size(self):
        pass

    @abstractmethod
    def size_in_use(self):
        pass

    @abstractmethod
    def space_in_raid(self):
        pass

    @abstractmethod
    def simulate_output(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, data):
        pass

    def destroy(self, drive):

        self.drives[drive] = None

    def clear(self):
        
        self.drives = [(bytearray(len(drive)) if drive != None else None) for drive in self.drives]
        self.used_space = 0

    @abstractmethod
    def recovery(self):
        pass
