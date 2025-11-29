#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox

def on_click():
    user_text = entry.get()
    messagebox.showinfo("Thông báo", f"Thằng chó của tao đã nhập: {user_text}")

root = tk.Tk()
root.title("OBF - PyCuTe v3.0")
root.geometry("350x200")

label = tk.Label(root, text="Nhập gì đó đi cu ?")
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack()

button = tk.Button(root, text="Bấm vào tao đi thằng chó !", command=on_click)
button.pack(pady=15)

root.mainloop()
