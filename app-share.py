import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
import requests
import os

SERVER_URL = "http://localhost:5000"

def upload_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        files = {'file': open(filepath, 'rb')}
        response = requests.post(f"{SERVER_URL}/upload", files=files)
        if response.status_code == 200:
            messagebox.showinfo("Thành công", "Đã tải lên file")
            refresh_file_list()
        else:
            messagebox.showerror("Lỗi", "Không thể tải lên file")

def refresh_file_list():
    response = requests.get(SERVER_URL)
    if response.status_code == 200:
        file_listbox.delete(0, tk.END)
        html = response.text
        # Trích xuất tên file từ HTML đơn giản
        import re
        files = re.findall(r'/download/(.*?)"', html)
        for f in files:
            file_listbox.insert(tk.END, f)
    else:
        messagebox.showerror("Lỗi", "Không thể lấy danh sách file")

def download_file():
    selected = file_listbox.curselection()
    if selected:
        filename = file_listbox.get(selected)
        response = requests.get(f"{SERVER_URL}/download/{filename}")
        if response.status_code == 200:
            save_path = filedialog.asksaveasfilename(initialfile=filename)
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                messagebox.showinfo("Thành công", f"Đã tải xuống: {filename}")
        else:
            messagebox.showerror("Lỗi", "Không thể tải file")

root = tk.Tk()
root.title("Giao diện chia sẻ file")

tk.Button(root, text="Tải lên file", command=upload_file).pack(pady=5)
tk.Button(root, text="Tải xuống file", command=download_file).pack(pady=5)

file_listbox = Listbox(root, width=50)
file_listbox.pack(pady=10)

refresh_file_list()

root.mainloop()