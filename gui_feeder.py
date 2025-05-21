import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import os
from datetime import datetime

# === Data Latih Dummy ===
data_latih = pd.DataFrame({
    "SuhuAir": [30.1, 30.5, 30.7, 31.0, 28.9, 29.5, 30.0],
    "SisaPakan": [50, 45, 46, 20, 80, 60, 55],
    "UmurUdang": [3, 10, 3, 25, 15, 15, 10],
    "JumlahPakan": [1.5, 1.45, 1.46, 1.2, 1.8, 1.6, 1.55],
    "PerluDiberiPakan": [1, 1, 1, 1, 0, 0, 1]
})

# === Training Decision Tree ===
X = data_latih[["SuhuAir", "SisaPakan", "UmurUdang", "JumlahPakan"]]
y = data_latih["PerluDiberiPakan"]
clf = DecisionTreeClassifier()
clf.fit(X, y)

# === Fungsi Klasifikasi dan Simpan ===
def klasifikasi():
    try:
        suhu = float(entry_suhu.get())
        sisa_pakan = float(entry_sisa.get())
        umur = int(entry_umur.get())
        jumlah_pakan = float(entry_jumlah.get())

        hasil = clf.predict([[suhu, sisa_pakan, umur, jumlah_pakan]])
        hasil_str = 'Ya' if hasil[0] == 1 else 'Tidak'
        label_hasil.config(text=f"Hasil Klasifikasi: {hasil_str}")

        waktu = datetime.now().strftime('%Y-%m-%d %H:%M')

        baris_baru = pd.DataFrame([[waktu, suhu, sisa_pakan, umur, jumlah_pakan, hasil_str]],
            columns=["Waktu", "Suhu Air (°C)", "Sisa Pakan (g)", "Umur Udang (hari)", "Jumlah Pakan (kg)", "Perlu Diberi Pakan"])

        if os.path.exists("data_feeder.xlsx"):
            data_lama = pd.read_excel("data_feeder.xlsx")
            data_baru = pd.concat([data_lama, baris_baru], ignore_index=True)
        else:
            data_baru = baris_baru

        data_baru.to_excel("data_feeder.xlsx", index=False)
        messagebox.showinfo("Sukses", "Data berhasil disimpan!")

    except ValueError:
        messagebox.showerror("Input Error", "Mohon masukkan angka yang valid!")

# === Fungsi Reset Input ===
def reset_input():
    entry_suhu.delete(0, tk.END)
    entry_sisa.delete(0, tk.END)
    entry_umur.delete(0, tk.END)
    entry_jumlah.delete(0, tk.END)
    label_hasil.config(text="Hasil Klasifikasi:")

# === Fungsi Tampilkan Pohon Keputusan ===
def tampilkan_pohon_decision_tree():
    plt.figure(figsize=(12, 8))
    plot_tree(clf,
              feature_names=["SuhuAir", "SisaPakan", "UmurUdang", "JumlahPakan"],
              class_names=["Tidak Diberi Pakan", "Perlu Diberi Pakan"],
              filled=True,
              rounded=True)
    plt.title("Struktur Pohon Keputusan untuk Smart Feeder Udang")
    plt.show()

# === Fungsi Tampilkan Data Klasifikasi ===
def tampilkan_data_klasifikasi():
    data_window = tk.Toplevel(root)
    data_window.title("Data Klasifikasi")
    data_window.geometry("1000x500")

    judul = tk.Label(data_window, text="Data Klasifikasi", font=("Helvetica", 14, "bold"))
    judul.pack(pady=10)

    frame_tombol = tk.Frame(data_window)
    frame_tombol.pack(pady=10)

    btn_refresh = tk.Button(frame_tombol, text="Refresh Data", command=refresh_tabel)
    btn_refresh.pack(side=tk.LEFT, padx=5)

    btn_close = tk.Button(frame_tombol, text="Tutup", command=data_window.destroy)
    btn_close.pack(side=tk.LEFT, padx=5)

    global tabel
    kolom = ["Waktu", "Suhu Air (°C)", "Sisa Pakan (g)", "Umur Udang (hari)", "Jumlah Pakan (kg)", "Perlu Diberi Pakan"]
    tabel = ttk.Treeview(data_window, columns=kolom, show="headings", height=15)

    for col in kolom:
        tabel.heading(col, text=col)
        tabel.column(col, width=140, anchor="center")

    tabel.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(data_window, orient="vertical", command=tabel.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tabel.configure(yscrollcommand=scrollbar.set)

    refresh_tabel()

# === Fungsi Refresh Data Tabel ===
def refresh_tabel():
    for item in tabel.get_children():
        tabel.delete(item)

    if os.path.exists("data_feeder.xlsx"):
        try:
            data = pd.read_excel("data_feeder.xlsx")
            for _, row in data.iterrows():
                tabel.insert("", "end", values=list(row))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {str(e)}")
    else:
        messagebox.showinfo("Info", "Belum ada data yang tersimpan")

# === GUI Utama ===
root = tk.Tk()
root.title("Sistem Smart Feeder Udang")
root.geometry("500x420")

frame_utama = tk.Frame(root)
frame_utama.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

judul_input = tk.Label(frame_utama, text="Input Data Monitoring", font=("Helvetica", 14, "bold"))
judul_input.pack(pady=(10, 20))

frame_input = tk.Frame(frame_utama)
frame_input.pack()

tk.Label(frame_input, text="Suhu Air (°C):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_suhu = tk.Entry(frame_input)
entry_suhu.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Sisa Pakan (g):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_sisa = tk.Entry(frame_input)
entry_sisa.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Umur Udang (hari):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_umur = tk.Entry(frame_input)
entry_umur.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Jumlah Pakan (kg):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_jumlah = tk.Entry(frame_input)
entry_jumlah.grid(row=3, column=1, padx=5, pady=5)

label_hasil = tk.Label(frame_utama, text="Hasil Klasifikasi:", font=("Arial", 12))
label_hasil.pack(pady=10)

frame_tombol = tk.Frame(frame_utama)
frame_tombol.pack(pady=20)

btn_oke = tk.Button(frame_tombol, text="Simpan Data", command=klasifikasi, bg="green", fg="white", width=15)
btn_oke.grid(row=0, column=0, padx=5)

btn_reset = tk.Button(frame_tombol, text="Reset", command=reset_input, bg="red", fg="white", width=15)
btn_reset.grid(row=0, column=1, padx=5)

btn_lihat_data = tk.Button(frame_tombol, text="Lihat Data Klasifikasi", command=tampilkan_data_klasifikasi, bg="blue", fg="white", width=20)
btn_lihat_data.grid(row=1, column=0, columnspan=2, pady=10)

btn_tree = tk.Button(frame_tombol, text="Lihat Pohon Keputusan", command=tampilkan_pohon_decision_tree)
btn_tree.grid(row=2, column=0, columnspan=2, pady=5)

# Jalankan GUI
root.mainloop()
