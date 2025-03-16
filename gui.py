import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from simulation.raid0 import Raid0Simulation
from simulation.raid1 import Raid1Simulation
from simulation.raid5 import Raid5Simulation
from simulation.raid10 import Raid10Simulation

# ตัวแปรเก็บสถานะระดับที่เลือก
raid = None

def confirm_level():
    if raid != None:
        center_frame.pack(side=tk.LEFT, padx=10)
        right_frame.pack(side=tk.LEFT, padx=10, pady=10)
        input_frame.pack(pady=10)  # แสดงช่องป้อนค่าใหม่ที่อยู่ด้านล่างปุ่มยืนยัน

        right_textbox.config(state="disable")
        center_textbox.config(state="disable")

def update_summary(total_data, used_data, remaining_data):

    summary_total.config(text=f"Capacity: {total_data} bytes")
    summary_used.config(text=f"Used: {used_data} bytes")
    summary_remaining.config(text=f"Space: {remaining_data} bytes")

def write_data():
    data = entry.get()
    
    if raid != None:
        if data:
            try:
                raid.write(data)
                entry.delete(0, tk.END)
                simulate()

            except ValueError as e:
                messagebox.showwarning("Error", e)
        else:
            messagebox.showwarning("Warning","Please specify the data.")
    else:
        messagebox.showwarning("Warining","Please choose raid level.")

def read_data():
    {}

def clear_data():
    {}

def restore_data():
    {}

def simulate():

    if raid != None:
        right_textbox.config(state="normal")
        right_textbox.delete(1.0, tk.END)
        right_textbox.insert(tk.END, raid.simulate_output())
        right_textbox.config(state="disable")
    else:
        messagebox.showwarning("Warining","Please choose raid level.")
    # right_listbox.delete(0, tk.END)
    # for item in data_list:
    #     right_listbox.insert(tk.END, item)

def calculate():

    global raid

    raid_level = level_combobox.get()
    drive_capacity = int(sizehdd_spinbox.get())
    drive_amount = int(amount_spinbox.get())

    drives = []
    for i in range(drive_amount):
        drives.append(drive_capacity)

    # print(f"RaidLevel: {raid_level}, DriveCapacity: {drive_capacity}, DriveAmount: {drive_amount}")
    # print(drives)
    
    try:
        if raid_level == "Raid 0":
            raid = Raid0Simulation(drives)
        elif raid_level == "Raid 1":
            raid = Raid1Simulation(drives)
        elif raid_level == "Raid 5":
            raid = Raid5Simulation(drives)
        elif raid_level == "Raid 10":
            raid = Raid10Simulation(drives)

        if raid != None:
            resize_window()
            confirm_level()
            update_summary(raid.total_size(), raid.size_in_use(), raid.space_in_raid())

            simulate()

    except ValueError as e:
        messagebox.showwarning("Error", e)
    

# main window
root = tk.Tk()
root.title("Raid Simulation")
root.geometry("300x300")
root.resizable(False,False)

def resize_window():
    root.geometry("1100x450")  # Change window size to 600x400

# **สร้างเฟรมด้านซ้าย** (เลือกระดับ)
left_frame = tk.Frame(root)
left_frame.pack(expand=True, side=tk.LEFT, padx=50, pady=10)

tk.Label(left_frame, text="Select Raid Level").pack()
level_combobox = ttk.Combobox(left_frame, values=["Raid 0", "Raid 1", "Raid 5", "Raid 10"], state="readonly", width=17)
level_combobox.pack(pady=5)
level_combobox.current(0)  # ตั้งค่าเริ่มต้นเป็น "ระดับ 0"

# # ปุ่มยืนยันระดับ
# confirm_button = tk.Button(left_frame, text="Confirm", command=lambda:[resize_window(),confirm_level(),confirm_button.pack_forget()], width=15)
# confirm_button.pack(pady=5)

# **แสดงผลสรุปข้อมูล (แยกเป็นบรรทัด)**
summary_total = tk.Label(left_frame, text="Capacity: -", font=("sans", 10))
summary_total.pack(pady=2)

summary_used = tk.Label(left_frame, text="Used: -", font=("Arial", 10))
summary_used.pack(pady=2)

summary_remaining = tk.Label(left_frame, text="Space: -", font=("Arial", 10))
summary_remaining.pack(pady=2)

# **เฟรมสำหรับช่องใส่ค่า (จะซ่อนตอนแรก)**
input_frame = tk.Frame(left_frame)


#สร้าง spinbox จำนวน raid 
tk.Label(input_frame, text="Select Drive Capacity").pack()
sizehdd_spinbox = tk.Spinbox(input_frame, from_=8,to=2048)
sizehdd_spinbox.pack(pady=5)

# สร้าง spinbox ขนาด harddisk
tk.Label(input_frame, text="Drives Amount").pack()
amount_spinbox = tk.Spinbox(input_frame,from_=2,to=10)
amount_spinbox.pack(pady=5)

custom_button = tk.Button(left_frame, text="Calculate", command=calculate, width=15) #*
custom_button.pack(pady=5)

# center frame (จะซ่อนอยู่ตอนแรก)**
center_frame = tk.Frame(root)

# widget in center frame
tk.Label(center_frame, text="Input Data").pack()
entry = tk.Entry(center_frame, width=50)
entry.pack(pady=5)
data = entry.get()

btn_write = tk.Button(center_frame, text="Write Data", command=write_data, width=15)
btn_write.pack(pady=5)

btn_clear = tk.Button(center_frame, text="Destroy Drive", command=clear_data, width=15)
btn_clear.pack(pady=5)

btn_restore = tk.Button(center_frame, text="Recovery Data", command=restore_data, width=15)
btn_restore.pack(pady=5)

btn_add = tk.Button(center_frame, text="Read Data", command=read_data, width=15)
btn_add.pack(pady=5)

# widget in center frame

# frame ย่อย
data_frame = tk.Frame(center_frame)
data_frame.pack(pady=5)

curr_data = tk.Label(center_frame, text="ข้อมูลปัจจุบัน :", font=("Arial", 10))
curr_data.pack(pady=5)

# **เพิ่ม Listbox สำหรับแสดงข้อมูลใต้ปุ่ม "อ่านข้อมูล"**
center_textbox = tk.Text(center_frame, width=30, height=11)
center_textbox.pack(pady=5)

# **สร้างเฟรมด้านขวา (ยังคงอยู่เหมือนเดิม)**
right_frame = tk.Frame(root)

tk.Label(right_frame, text="Simulation").pack()
right_textbox = tk.Text(right_frame, width=100, height=25)


simulate_button = tk.Button(right_frame, text="Simulate Output", command=simulate, width=15)
simulate_button.pack(pady=10)

right_textbox.pack()

# เริ่มรัน GUI
root.mainloop()