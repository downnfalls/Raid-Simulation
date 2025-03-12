import os

class RAID0:
    def __init__(self, disks, chunk_size=4): #init raid0, disks: รายชื่อไฟล์ดิสก์ที่ใช้,chunk_size: ขนาดของข้อมูลที่แบ่งแต่ละดิสก์ (bytes)

        self.disks = disks
        self.num_disks = len(disks) #จำนวนdisk
        self.chunk_size = chunk_size

    def write(self, data): #มีselfกับdata
        #ตัดข้อมูลdataตามi data[start:stop] //กำหนดcs=4 ตัดทีละ4
        #for i in range(start:stop:step)
        chunks = [data[i:i + self.chunk_size] for i in range(0, len(data), self.chunk_size)] 
        #range(start:stop:step)

        #for i, a in enumerate(chunks)
        for i, chunk in enumerate(chunks): #iตามจำนวนข้อมูลchunks
            disk_index = i % self.num_disks  # i mod จำนวนดิสก์
            with open(self.disks[disk_index], "ab") as file: #append binary 
                file.write(chunk) 


    def read(self): #อ่านข้อมูลจาก RAID 0
        data = b"" #byte string represent in ASCII
        chunk_lists = [[] for _ in range(self.num_disks)]
        #For each number in the range, an empty list ([]) is created.
        # _ is a common variable name used when the value of the iteration variable is not needed.
        # The result is a list containing self.num_disks number of empty lists.
        #สร้างลิสต์เปล่า -> [] ตามจำนวน disk

        # อ่านข้อมูลจากแต่ละดิสก์
        for i, disk in enumerate(self.disks):
            with open(disk, "rb") as file: #read-binary
                chunk_lists[i] = [file.read(self.chunk_size) for _ in range(os.path.getsize(disk) // self.chunk_size)]
                #os.pathเข้าถึงไฟล์
        # รวมข้อมูลกลับเป็นไฟล์เดียว
        for i in range(max(map(len, chunk_lists))): #วิ่งตามความยาวchunkที่ยาวสุด
            for chunk_list in chunk_lists:
                if i < len(chunk_list):
                    data += chunk_list[i]

        return data

    def format_disks(self):#ลบraid
        for disk in self.disks:
            open(disk, "wb").close() #write binary เปิดไฟล์เพื่อเขียนทับ ปิดไฟล์