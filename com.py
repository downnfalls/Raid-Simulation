import math

class HDD:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
    
    def getCapacity(self):
        return self.capacity

class RAID:
    deleted_raids = {}
    
    def __init__(self, name, level):
        self.RAID_LS = []
        self.name = name
        self.level = level
    
    def addHDD(self, hdd):
        self.RAID_LS.append(hdd)
    
    def getSUMcapacity(self):
        if not self.RAID_LS:
            return "No HDDs in RAID"
        
        min_capacity = min(hdd.getCapacity() for hdd in self.RAID_LS)
        num_disks = len(self.RAID_LS)
        
        if self.level == 0:
            return sum(hdd.getCapacity() for hdd in self.RAID_LS)
        elif self.level == 1:
            return (num_disks // 2) * min_capacity
        elif self.level == 5:
            return (num_disks - 1) * min_capacity
        elif self.level == 6:
            return (num_disks - 2) * min_capacity
        elif self.level == 10:
            return (num_disks // 2) * min_capacity
        else:
            return "Unsupported RAID level"
    
    def expandRAID(self, new_hdd):
        if self.level == 0:
            self.RAID_LS.append(new_hdd)
            return f"RAID 0 expanded. New capacity: {self.getSUMcapacity()} GB"

        elif self.level == 1:
            if len(self.RAID_LS) % 2 == 0:
                return "RAID 1 requires an even number of drives."
            self.RAID_LS.append(new_hdd)
            return f"RAID 1 expanded. New capacity: {self.getSUMcapacity()} GB"

        elif self.level == 5:
            self.RAID_LS.append(new_hdd)
            return f"RAID 5 expanded. New capacity: {self.getSUMcapacity()} GB"

        elif self.level == 6:
            self.RAID_LS.append(new_hdd)
            return f"RAID 6 expanded. New capacity: {self.getSUMcapacity()} GB"

        elif self.level == 10:
            if len(self.RAID_LS) % 2 == 1:
                return "RAID 10 requires an even number of drives."
            self.RAID_LS.append(new_hdd)
            return f"RAID 10 expanded. New capacity: {self.getSUMcapacity()} GB"

        else:
            return "RAID expansion for this level is not supported."
    
    def deleteRAID(self):
        RAID.deleted_raids[self.name] = self.RAID_LS.copy()
        self.RAID_LS.clear()
        return f"RAID {self.name} has been deleted."
    
    def restoreRAID(self):
        if self.name in RAID.deleted_raids:
            self.RAID_LS = RAID.deleted_raids.pop(self.name)
            return f"RAID {self.name} has been restored."
        return "No backup found for this RAID."
    
    def checkIntegrity(self):
        if not self.RAID_LS:
            return "No HDDs in RAID to check integrity."
        
        num_disks = len(self.RAID_LS)
        if self.level == 1 and num_disks < 2:
            return "RAID 1 requires at least 2 disks for redundancy."
        elif self.level == 5 and num_disks < 3:
            return "RAID 5 requires at least 3 disks for parity."
        elif self.level == 6 and num_disks < 4:
            return "RAID 6 requires at least 4 disks for dual parity."
        elif self.level == 10 and num_disks < 4:
            return "RAID 10 requires at least 4 disks for mirroring and striping."
        
        return "RAID structure appears to be intact."

# Example Usage
hdd1 = HDD("Disk1", 1000)
hdd2 = HDD("Disk2", 1000)
hdd3 = HDD("Disk3", 1000)
raid5 = RAID("RAID 5 System", 5)
raid5.addHDD(hdd1)
raid5.addHDD(hdd2)
raid5.addHDD(hdd3)

print(f"Before expansion: {raid5.getSUMcapacity()} GB")

new_hdd = HDD("Disk4", 1000)
print(raid5.expandRAID(new_hdd))

print(f"After expansion: {raid5.getSUMcapacity()} GB")

print(raid5.deleteRAID())  # Deleting the RAID
print(raid5.restoreRAID())  # Restoring the RAID
print(raid5.checkIntegrity())  # Checking RAID integrity
