import tkinter as tk
from tkinter import ttk
import pandas as pd

# Baca data dari Excel
data = pd.read_excel("data_feeder.xlsx")  # Ganti dengan nama file kamu

# Buat window utama
root = tk.Tk()
root.title("Sistem Smart Feeder Udang")
root.geometry("900x300")

# Buat frame tabel
frame = ttk.Frame(root)
frame.pack(pady=20)

# Buat Treeview untuk menampilkan data
tree = ttk.Treeview(frame)
tree["columns"] = list(data.columns)
tree["show"] = "headings"

# Atur header kolom
for col in data.columns:
    tree.heading(col, text=col)
    tree.column(col, width=130, anchor="center")

# Masukkan data ke tabel
for _, row in data.iterrows():
    tree.insert("", tk.END, values=list(row))

tree.pack()

# Jalankan GUI
root.mainloop()
