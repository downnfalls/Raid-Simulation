import tkinter as tk
from tkinter import * #ttk (themed Tkinter) สร้าง UI ที่มีลักษณะและการออกแบบที่ดีกว่า โดยเฉพาะ widgets เช่น ปุ่ม, กล่องข้อความ, และเมนู 

window = tk.Tk()  
window.geometry('1024x720')  # กำหนดขนาดหน้าต่าง
window.title('RAID SIMULATION')  # ตั้งชื่อหน้าต่าง
window.config(bg='pink')  # กำหนดสีพื้นหลัง

if window.winfo_exists():
    frame = tk.Frame(window, width=500, height=300, bg="gray")
    frame.pack()
    btn=tk.Button(window, text="Click")
    btn.pack()

    # กรอบด้านบนสำหรับปุ่มควบคุม
    TOP_FRAME = tk.Frame(window, height=80, bg='#1B1A55')
    TOP_FRAME.pack(side=tk.TOP, fill=tk.X)

    # กรอบด้านซ้าย (HDD List)
    LEFT_FRAME = tk.Frame(window, width=300, bg='#535C91')
    LEFT_FRAME.pack(side=tk.LEFT, fill=tk.Y)

    # กรอบด้านขวา (RAID List)
    RIGHT_FRAME = tk.Frame(window, bg='#9290C3')
    RIGHT_FRAME.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    # ปุ่มเพิ่ม HDD
    btn_add_hdd = tk.Button(TOP_FRAME, text="Add HDD", bg='#9290C3', command=lambda: print("Add HDD Clicked"))
    btn_add_hdd.pack(side=tk.LEFT, padx=20, pady=10)

    # ปุ่มเพิ่ม RAID
    btn_add_raid = tk.Button(TOP_FRAME, text="Add RAID", bg='#9290C3', command=lambda: print("Add RAID Clicked"))
    btn_add_raid.pack(side=tk.LEFT, padx=20, pady=10)

    # ปุ่มลบ RAID
    btn_delete_raid = tk.Button(TOP_FRAME, text="Delete RAID", bg='#9290C3', command=lambda: print("Delete RAID Clicked"))
    btn_delete_raid.pack(side=tk.LEFT, padx=20, pady=10)



window.mainloop()  # รัน GUI