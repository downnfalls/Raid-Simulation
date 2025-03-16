from simulation.raid0 import Raid0Simulation
from simulation.raid1 import Raid1Simulation
from simulation.raid5 import Raid5Simulation
from simulation.raid10 import Raid10Simulation

if __name__ == "__main__":
    # Simulating 3 drives with 1024 bytes each
    raid = Raid1Simulation([16, 16, 16, 16])

    print(f"Total Size: {raid.total_size()}")
    print(f"Used: {raid.size_in_use()}")
    print(f"Space: {raid.space_in_raid()}")

    print("Initial drives:")
    print(raid.simulate_output())

    # Writing data to the RAID 0
    data_to_write = input("Specify data: ")
    print("\nWriting data:")
    raid.write(data_to_write)

    # Reading data from the RAID 0
    print("\nReading data:")
    data_read = raid.read()
    print(f"Data read: {data_read}")

    # Final drives state
    print("\nFinal drives after write:")
    print(raid.simulate_output())

    print(f"Total Size: {raid.total_size()}")
    print(f"Used: {raid.size_in_use()}")
    print(f"Space: {raid.space_in_raid()}")

    print(f"\nDestroying: ")
    raid.destroy(3)
    print(raid.simulate_output())

    print(f"Data read: {raid.read()}")

    print(f"\nRecovering: ")
    raid.recovery()
    print(raid.simulate_output())

    print(f"Data read: {raid.read()}")

    # abcdefghijklmnopqrstuvwxyz