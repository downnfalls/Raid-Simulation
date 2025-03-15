import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# ตัวแปรเก็บสถานะระดับที่เลือก
selected_level = None
data_list = []  # เก็บข้อมูลที่ป้อนเข้าไป

def confirm_level():
    global selected_level
    selected_level = level_combobox.get()

    # แสดงผลในส่วนของข้อมูลรวม
    update_summary()

    # แสดงส่วนกลางและช่องป้อนค่าหลังจากยืนยันระดับ
    if selected_level:
        center_frame.pack(side=tk.LEFT, padx=10)
        right_frame.pack(side=tk.LEFT, padx=10, pady=10)
        input_frame.pack(pady=10)  # แสดงช่องป้อนค่าใหม่ที่อยู่ด้านล่างปุ่มยืนยัน
        messagebox.showinfo("ยืนยันระดับ", f"คุณเลือกระดับ: {selected_level}")

def update_summary():
    total_data = len(data_list)  # จำนวนข้อมูลทั้งหมดที่ใส่ไป
    used_data = total_data  # จำนวนที่ใช้ไป
    remaining_data = max(0, 10 - used_data)  # สมมติว่าให้ใส่ได้สูงสุด 10 รายการ

    summary_total.config(text=f"รวมข้อมูล: {total_data}")
    summary_used.config(text=f"ใช้ไป: {used_data}")
    summary_remaining.config(text=f"เหลือ: {remaining_data}")

def add_data():
    text = entry.get()
    if text:
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
    entry.delete(0, tk.END)

def display_data_center():
    """ แสดงข้อมูลในส่วนกลางใต้ปุ่ม 'อ่านข้อมูล' """
    center_listbox.delete(0, tk.END)
    for item in data_list:
        center_listbox.insert(tk.END, item)

def display_data_right():
    """ แสดงข้อมูลในหน้าด้านขวา """
    right_listbox.delete(0, tk.END)
    for item in data_list:
        right_listbox.insert(tk.END, item)

def add_custom_value():
    value = custom_entry.get()
    if value:
        data_list.append(value)
        update_summary()
        display_data_center()
        display_data_right()
        custom_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("คำเตือน", "กรุณากรอกค่า")

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("ระบบจัดการข้อมูล")
root.geometry("800x450")  # ขยายขนาดหน้าต่างให้พอดีกับหน้าด้านขวา

# **สร้างเฟรมด้านซ้าย** (เลือกระดับ)
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(left_frame, text="เลือกระดับ").pack()
level_combobox = ttk.Combobox(left_frame, values=["ระดับ 1", "ระดับ 2", "ระดับ 3", "ระดับ 4", "ระดับ 5"], state="readonly", width=17)
level_combobox.pack(pady=5)
level_combobox.current(0)  # ตั้งค่าเริ่มต้นเป็น "ระดับ 1"

# ปุ่มยืนยันระดับ
confirm_button = tk.Button(left_frame, text="ยืนยันระดับ", command=confirm_level, width=15)
confirm_button.pack(pady=5)

# **แสดงผลสรุปข้อมูล (แยกเป็นบรรทัด)**
summary_total = tk.Label(left_frame, text="รวมข้อมูล: -", font=("Arial", 10))
summary_total.pack(pady=2)

summary_used = tk.Label(left_frame, text="ใช้ไป: -", font=("Arial", 10))
summary_used.pack(pady=2)

summary_remaining = tk.Label(left_frame, text="เหลือ: -", font=("Arial", 10))
summary_remaining.pack(pady=2)

# **เฟรมสำหรับช่องใส่ค่า (จะซ่อนตอนแรก)**
input_frame = tk.Frame(left_frame)

tk.Label(input_frame, text="ใส่ค่าเพิ่มเติม").pack()
custom_entry = tk.Entry(input_frame, width=20)
custom_entry.pack(pady=5)

custom_button = tk.Button(input_frame, text="เพิ่มค่า", command=add_custom_value, width=15)
custom_button.pack(pady=5)

# **สร้างเฟรมตรงกลาง (จะซ่อนอยู่ตอนแรก)**
center_frame = tk.Frame(root)

tk.Label(center_frame, text="ใส่ข้อมูล").pack()
entry = tk.Entry(center_frame, width=20)
entry.pack(pady=5)

btn_clear = tk.Button(center_frame, text="ลบข้อมูล", command=clear_data, width=15)
btn_clear.pack(pady=5)

btn_restore = tk.Button(center_frame, text="กู้คืนข้อมูล", command=restore_data, width=15)
btn_restore.pack(pady=5)

btn_add = tk.Button(center_frame, text="อ่านข้อมูล", command=add_data, width=15)
btn_add.pack(pady=5)

# **เพิ่ม Listbox สำหรับแสดงข้อมูลใต้ปุ่ม "อ่านข้อมูล"**
center_listbox = tk.Listbox(center_frame, width=30, height=11)
center_listbox.pack(pady=5)

# **สร้างเฟรมด้านขวา (ยังคงอยู่เหมือนเดิม)**
right_frame = tk.Frame(root)

tk.Label(right_frame, text="ผลลัพธ์ที่ได้").pack()
right_listbox = tk.Listbox(right_frame, width=30, height=20)
right_listbox.pack()

# เริ่มรัน GUI
root.mainloop()