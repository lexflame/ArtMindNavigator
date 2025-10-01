from tkinter import filedialog, messagebox

def select_file_path(title="Выберите файл", def_ext=".txt", filetypes=[("Text files","*.txt")]):
    path = filedialog.asksaveasfilename(title=title, defaultextension=def_ext, filetypes=filetypes)
    if path:
        messagebox.showinfo("Файл выбран", f"Файл: {path}")
    return path
