import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# ตัวแปรเก็บสถานะระดับที่เลือก
selected_level = None
data_list = []  # เก็บข้อมูลที่ป้อนเข้าไป
value1 = 0
size_disk = 0
amount = 1
total = 0

def confirm_level():
    global selected_level
    selected_level = level_combobox.get()

    # แสดงผลในส่วนของข้อมูลรวม
    update_summary()

    if selected_level=="ระดับ 0":
        btn_restore.config(state=tk.DISABLED)
    else: btn_restore.config(state=tk.NORMAL)

    # แสดงส่วนกลางและช่องป้อนค่าหลังจากยืนยันระดับ
    if selected_level:
        center_frame.pack(side=tk.LEFT, padx=10)
        right_frame.pack(side=tk.LEFT, padx=10, pady=10)
        input_frame.pack(pady=10)  # แสดงช่องป้อนค่าใหม่ที่อยู่ด้านล่างปุ่มยืนยัน
        messagebox.showinfo("ยืนยันระดับ", f"คุณเลือกระดับ: {selected_level}")

def update_summary():
    global total
    total_data = total  # จำนวนข้อมูลทั้งหมดที่ใส่ไป
    #size_disk = int(custom_entry.get())
    #total_data = size_disk*amount
    used_data = total_data  # จำนวนที่ใช้ไป ค่อยคำนวณจากดาต้าที่ใส่
    remaining_data = max(0, 10 - used_data)  # สมมติว่าให้ใส่ได้สูงสุด 10 รายการ

    summary_total.config(text=f"ขนาดดิสก์สุทธิ: {total_data}")
    summary_used.config(text=f"ใช้ไป: {used_data}")
    summary_remaining.config(text=f"เหลือ: {remaining_data}")

def write_data():
    text = entry.get()
    if text:
        center_textbox.insert(tk.END,text)
        entry.delete(0,tk.END)
    else:
        messagebox.showwarning("คำเตือน","กรุณากรอกข้อมูล")

def read_data(): # อ่านข้อมูล
    text = entry.get()
    if text:
        center_textbox.delete("1.0",data)
        data_list.append(text)
        update_summary()
        display_data_center()  # แสดงข้อมูลในส่วนกลาง
        display_data_right()  # แสดงผลด้านขวา
        entry.delete(0, tk.END)  # ล้างช่องป้อนข้อมูล
    else:
        messagebox.showwarning("คำเตือน", "กรุณากรอกข้อมูล")

def clear_data():
    data_list.clear()
    update_summary()
    display_data_center()  # เคลียร์ข้อมูลในส่วนกลาง
    display_data_right()  # เคลียร์ข้อมูลด้านขวา

def restore_data():
    global selected_level
    entry.delete(0, tk.END)

def display_data_center():
    """ แสดงข้อมูลในส่วนกลางใต้ปุ่ม 'อ่านข้อมูล' """
    center_textbox.delete("1.0", tk.END) # ล้างข้อมูลเก่า
    center_textbox.insert(tk.END, data)  # ใส่ค่าจากตัวแปร

def display_data_right():
    right_listbox.delete(0, tk.END)
    for item in data_list:
        right_listbox.insert(tk.END, item)

def add_custom_value():
    total = amount*sizehdd

    # global value1
    # value = int(custom_entry.get()) #convert string to int
    # if value:
    #     try:
    #         num_value=int(value)
    #         value1+=value
    #         data_list.append(value)
    #         update_summary()
    #         display_data_center()
    #         display_data_right()
    #         custom_entry.delete(0, tk.END) #clear input field
    #     except ValueError:
    #         messagebox.showwarning("ข้อผิดพลาด", "กรุณากรอกตัวเลขเท่านั้น")
    # else:
    #     messagebox.showwarning("คำเตือน", "กรุณากรอกค่า")

# main window
root = tk.Tk()
root.title("ระบบจัดการข้อมูล")
root.geometry("200x200")
root.resizable(False,False)

def resize_window():
    root.geometry("800x450")  # Change window size to 600x400

# **สร้างเฟรมด้านซ้าย** (เลือกระดับ)
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=50, pady=10)

tk.Label(left_frame, text="เลือกระดับ").pack()
level_combobox = ttk.Combobox(left_frame, values=["ระดับ 0", "ระดับ 1", "ระดับ 2", "ระดับ 3", "ระดับ 4", "ระดับ 5"], state="readonly", width=17)
level_combobox.pack(pady=5)
level_combobox.current(0)  # ตั้งค่าเริ่มต้นเป็น "ระดับ 0"

# ปุ่มยืนยันระดับ
confirm_button = tk.Button(left_frame, text="ยืนยันระดับ", command=lambda:[resize_window(),confirm_level()], width=15)
confirm_button.pack(pady=5)

# **แสดงผลสรุปข้อมูล (แยกเป็นบรรทัด)**
summary_total = tk.Label(left_frame, text="ขนาดดิสก์สุทธิ: -", font=("Arial", 10))
summary_total.pack(pady=2)

summary_used = tk.Label(left_frame, text="ใช้ไป: -", font=("Arial", 10))
summary_used.pack(pady=2)

summary_remaining = tk.Label(left_frame, text="เหลือ: -", font=("Arial", 10))
summary_remaining.pack(pady=2)

# **เฟรมสำหรับช่องใส่ค่า (จะซ่อนตอนแรก)**
input_frame = tk.Frame(left_frame)


#สร้าง spinbox จำนวน raid 
tk.Label(input_frame, text="ใส่ขนาด harddisk").pack()
amount_spinbox = tk.Spinbox(input_frame, from_=1,to=100000)
amount_spinbox.pack(pady=5)
amount=int(amount_spinbox.get())

# สร้าง spinbox ขนาด harddisk
tk.Label(input_frame, text="ใส่จำนวน harddisk").pack()
sizehdd_spinbox = tk.Spinbox(input_frame,from_=1,to=1000)
sizehdd_spinbox.pack(pady=5)
sizehdd = int(sizehdd_spinbox.get())

custom_button = tk.Button(input_frame, text="Apply", command=add_custom_value, width=15) #*
custom_button.pack(pady=5)

# center frame (จะซ่อนอยู่ตอนแรก)**
center_frame = tk.Frame(root)

# widget in center frame
tk.Label(center_frame, text="ใส่ข้อมูล").pack()
entry = tk.Entry(center_frame, width=50)
entry.pack(pady=5)
data = entry.get()

btn_write = tk.Button(center_frame, text="เขียนข้อมูล", command=write_data, width=15)
btn_write.pack(pady=5)

btn_clear = tk.Button(center_frame, text="ลบข้อมูล", command=clear_data, width=15)
btn_clear.pack(pady=5)

btn_restore = tk.Button(center_frame, text="กู้คืนข้อมูล", command=restore_data, width=15)
btn_restore.pack(pady=5)

btn_add = tk.Button(center_frame, text="อ่านข้อมูล", command=read_data, width=15)
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

tk.Label(right_frame, text="ผลลัพธ์ที่ได้").pack()
right_listbox = tk.Listbox(right_frame, width=30, height=20)
right_listbox.pack()

# เริ่มรัน GUI
root.mainloop()