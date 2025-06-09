import tkinter as tk
from tkinter import messagebox, simpledialog
import os
from datetime import datetime

daftar_tugas = []

def tampilkan_tugas(tugas_filter=None):
    """Menampilkan daftar tugas pada listbox_tugas. Jika ada filter, tampilkan hasil filter."""
    listbox_tugas.delete(0, tk.END)
    data = tugas_filter if tugas_filter else daftar_tugas
    for i, (tugas, deadline) in enumerate(data):
        listbox_tugas.insert(tk.END, f"{i+1}. {tugas} - Deadline: {deadline}")
        try:
            deadline_date = datetime.strptime(deadline, "%d-%m-%Y").date()
            if deadline_date < datetime.today().date():
                listbox_tugas.itemconfig(i, {'fg': 'red'})
            else:
                listbox_tugas.itemconfig(i, {'fg': 'black'})
        except ValueError:
            listbox_tugas.itemconfig(i, {'fg': 'orange'})

def tambah_tugas():
    """Menambah tugas baru ke daftar_tugas setelah validasi input."""
    tugas = entry_tugas.get()
    deadline = entry_deadline.get()
    try:
        datetime.strptime(deadline, "%d-%m-%Y")
    except ValueError:
        messagebox.showerror("Format Salah", "Deadline harus format DD-MM-YYYY!")
        return
    if tugas and deadline:
        daftar_tugas.append([tugas, deadline])
        entry_tugas.delete(0, tk.END)
        entry_deadline.delete(0, tk.END)
        tampilkan_tugas()
    else:
        messagebox.showwarning("Input Kosong", "Isi kedua kolom terlebih dahulu!")

def hapus_tugas():
    """Menghapus tugas yang dipilih dari daftar_tugas."""
    index = listbox_tugas.curselection()
    if index:
        daftar_tugas.pop(index[0])
        tampilkan_tugas()
    else:
        messagebox.showwarning("Tidak ada pilihan", "Pilih tugas yang ingin dihapus!")

def edit_tugas():
    """Mengedit tugas yang dipilih, termasuk validasi deadline."""
    index = listbox_tugas.curselection()
    if index:
        tugas_baru = simpledialog.askstring("Edit Tugas", "Masukkan tugas baru:", initialvalue=daftar_tugas[index[0]][0])
        deadline_baru = simpledialog.askstring("Edit Deadline", "Masukkan deadline baru (DD-MM-YYYY):", initialvalue=daftar_tugas[index[0]][1])
        if tugas_baru and deadline_baru:
            try:
                datetime.strptime(deadline_baru, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Format Salah", "Deadline harus format DD-MM-YYYY!")
                return
            daftar_tugas[index[0]] = [tugas_baru, deadline_baru]
            tampilkan_tugas()
    else:
        messagebox.showwarning("Tidak ada pilihan", "Pilih tugas yang ingin diedit!")

def simpan_ke_file():
    """Menyimpan daftar_tugas ke file tugas.txt."""
    with open("tugas.txt", "w", encoding="utf-8") as file:
        for tugas, deadline in daftar_tugas:
            file.write(f"{tugas}||{deadline}\n")

def muat_dari_file():
    """Memuat daftar_tugas dari file tugas.txt, mencegah duplikasi data."""
    daftar_tugas.clear()
    if os.path.exists("tugas.txt"):
        print("File ditemukan, memuat data...")  # Debug
        try:
            with open("tugas.txt", "r", encoding="utf-8") as file:
                for baris in file:
                    print("Baris:", baris)  # Debug
                    parts = baris.strip().split("||")
                    if len(parts) == 2:
                        daftar_tugas.append(parts)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat file: {e}")
    tampilkan_tugas()

def cari_tugas():
    """Mencari tugas berdasarkan keyword pada entry_cari."""
    keyword = entry_cari.get().lower()
    hasil = [item for item in daftar_tugas if keyword in item[0].lower()]
    tampilkan_tugas(hasil)

def filter_deadline():
    """Memfilter tugas berdasarkan tanggal deadline pada entry_filter."""
    tanggal = entry_filter.get()
    hasil = [item for item in daftar_tugas if tanggal == item[1]]
    tampilkan_tugas(hasil)

def tampilkan_semua():
    """Menampilkan semua tugas tanpa filter."""
    tampilkan_tugas()

# GUI Setup
root = tk.Tk()
root.title("To-Do List Sederhana")
root.geometry("420x580")

tk.Label(root, text="Tugas:").pack()
entry_tugas = tk.Entry(root, width=50)
entry_tugas.pack()

tk.Label(root, text="Deadline (DD-MM-YYYY):").pack()
entry_deadline = tk.Entry(root, width=50)
entry_deadline.pack()

tk.Button(root, text="Tambah Tugas", command=tambah_tugas).pack(pady=5)

listbox_tugas = tk.Listbox(root, width=60)
listbox_tugas.pack(pady=10)

tk.Button(root, text="Hapus Tugas", command=hapus_tugas).pack(pady=2)
tk.Button(root, text="Edit Tugas", command=edit_tugas).pack(pady=2)

tk.Label(root, text="Cari Tugas:").pack()
entry_cari = tk.Entry(root, width=40)
entry_cari.pack()
tk.Button(root, text="Cari", command=cari_tugas).pack(pady=2)

tk.Label(root, text="Filter Deadline (DD-MM-YYYY):").pack()
entry_filter = tk.Entry(root, width=40)
entry_filter.pack()
tk.Button(root, text="Filter", command=filter_deadline).pack(pady=2)
tk.Button(root, text="Tampilkan Semua", command=tampilkan_semua).pack(pady=2)

muat_dari_file()
root.protocol("WM_DELETE_WINDOW", lambda: (simpan_ke_file(), root.destroy()))
root.mainloop()