import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # ใช้ ttk สำหรับ Combobox

# ฟังก์ชันเมื่อกดปุ่ม
def increase_size():
    texts = [entry1.get(), entry2.get(), entry3.get(), entry4.get()]
    texts = [text.upper() for text in texts if text]  # แปลงเป็นตัวพิมพ์ใหญ่ (ถ้ามีข้อความ)
    if texts:
        listbox.insert(tk.END, f"ขยาย: {' '.join(texts)}")
    else:
        messagebox.showwarning("คำเตือน", "กรุณากรอกข้อความ")

def clear_data():
    listbox.delete(0, tk.END)

def restore_data():
    for entry in [entry1, entry2, entry3, entry4]:
        entry.delete(0, tk.END)

def check_data():
    items = listbox.get(0, tk.END)
    if items:
        messagebox.showinfo("ตรวจสอบข้อมูล", "\n".join(items))
    else:
        messagebox.showinfo("ตรวจสอบข้อมูล", "ไม่มีข้อมูล")

def select_level():
    level = level_combobox.get()
    if level:
        messagebox.showinfo("RAID level", f"คุณเลือก : {level}")
    else:
        messagebox.showwarning("คำเตือน", "กรุณาเลือก RAID level")

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("RAID")
root.geometry("550x400")

# **สร้างเฟรมด้านซ้าย** (ใส่ข้อความ)
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(left_frame, text="ชื่อ HDD").pack()
entry1 = tk.Entry(left_frame, width=20)
entry1.pack(pady=5)

tk.Label(left_frame, text="ขนาดความจุ HDD").pack()
entry2 = tk.Entry(left_frame, width=20)
entry2.pack(pady=5)

tk.Label(left_frame, text="ชื่อ RAID").pack()
entry3 = tk.Entry(left_frame, width=20)
entry3.pack(pady=5)

tk.Label(left_frame, text="ขนาดความจุ RAID").pack()
entry4 = tk.Entry(left_frame, width=20)
entry4.pack(pady=5)

# **สร้างเฟรมตรงกลาง** (ปุ่มควบคุม)
center_frame = tk.Frame(root)
center_frame.pack(side=tk.LEFT, padx=10)

btn1 = tk.Button(center_frame, text="เพิ่มขนาด", command=increase_size, width=15)
btn1.pack(pady=5)

btn2 = tk.Button(center_frame, text="ลบข้อมูล", command=clear_data, width=15)
btn2.pack(pady=5)

btn3 = tk.Button(center_frame, text="กู้คืนข้อมูล", command=restore_data, width=15)
btn3.pack(pady=5)

btn4 = tk.Button(center_frame, text="ตรวจสอบข้อมูล", command=check_data, width=15)
btn4.pack(pady=5)

# **Dropdown เลือกระดับ**
tk.Label(center_frame, text="เลือก RAID Level").pack()
level_combobox = ttk.Combobox(center_frame, values=["RAID 0", "RAID 1", "RAID 5", "RAID 6", "RAID 10"], state="readonly", width=17)
level_combobox.pack(pady=5)
level_combobox.current(0)  # ตั้งค่าให้เลือก "ระดับ 1" เป็นค่าเริ่มต้น

# **ปุ่มยืนยันระดับ**
level_button = tk.Button(center_frame, text="confirm", command=select_level, width=15)
level_button.pack(pady=5)

# **สร้างเฟรมด้านขวา** (แสดงรายการผลลัพธ์)
right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(right_frame, text="รายการผลลัพธ์").pack()
listbox = tk.Listbox(right_frame, width=30, height=12)
listbox.pack()

# เริ่มรัน GUI
root.mainloop()
