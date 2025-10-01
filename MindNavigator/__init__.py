import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os, json

CONFIG_FILE = "config.json"

class DarkTheme:
    def __init__(self):
        self.bg_color = "#2C2F33"
        self.fg_color = "#FFFFFF"
        self.accent_color = "#7289DA"
        self.entry_bg = "#36393F"
        self.entry_fg = "#FFFFFF"
        self.button_bg = "#23272A"
        self.button_fg = "#FFFFFF"
        self.tab_bg = "#36393F"
        self.tab_fg = "#FFFFFF"
        self.tab_selected_bg = "#444850"
        self.tab_selected_fg = "#FFFFFF"


class MultiTabApp:
    def __init__(self, root):
        self.root = root
        self.theme = DarkTheme()
        self.root.title("MindNavigator")
        self.root.config(bg=self.theme.bg_color)
        self.tasks = []

        # Загружаем настройки
        self.config = self.load_config()
        self.current_profile = self.config.get("current_profile", "Default")
        if "profiles" not in self.config:
            self.config["profiles"] = {"Default": "notes.txt"}
        self.notes_file = self.config["profiles"][self.current_profile]

        # Меню
        self.create_menu()

        # Notebook (вкладки)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill=tk.BOTH)

        # Настройка стиля
        self.style = ttk.Style()
        self.style.theme_create("DarkStyle", parent="alt", settings={
            "TNotebook": {
                "configure": {"background": self.theme.bg_color, "tabmargins": [2, 2, 2, 0]},
                "map": {"background": [("selected", self.theme.tab_selected_bg)],
                        "foreground": [("selected", self.theme.tab_selected_fg)]}
            },
            "TNotebook.Tab": {
                "configure": {"background": self.theme.tab_bg, "foreground": self.theme.tab_fg,
                              "padding": [10, 5], "font": ("Helvetica", 10)},
                "map": {"background": [("selected", self.theme.tab_selected_bg)],
                        "expand": [("selected", [1, 1, 1, 0])]}
            }
        })
        self.style.theme_use("DarkStyle")

        # Фреймы для вкладок
        self.task_frame = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.map_frame = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.note_frame = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.nav_frame = tk.Frame(self.notebook, bg=self.theme.bg_color)

        # Добавляем вкладки
        self.notebook.add(self.task_frame, text="Задачи")
        self.notebook.add(self.map_frame, text="Карты")
        self.notebook.add(self.note_frame, text="Заметки")
        self.notebook.add(self.nav_frame, text="Навигатор")

        # Виджеты
        self.create_task_widgets()
        self.create_map_widgets()
        self.create_note_widgets()
        self.create_nav_widgets()

        # Загружаем заметки
        self.load_notes()

    # ================== МЕНЮ ==================
    def create_menu(self):
        menubar = tk.Menu(self.root, bg=self.theme.bg_color, fg=self.theme.fg_color, tearoff=0)

        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.theme.bg_color, fg=self.theme.fg_color)
        file_menu.add_command(label="Настройки", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        # Меню Профиль заметок
        self.profile_menu = tk.Menu(menubar, tearoff=0, bg=self.theme.bg_color, fg=self.theme.fg_color)
        self.profile_var = tk.StringVar(value=self.current_profile)
        self.update_profile_menu()
        menubar.add_cascade(label="Профиль заметок", menu=self.profile_menu)

        self.root.config(menu=menubar)

    def update_profile_menu(self):
        self.profile_menu.delete(0, tk.END)
        for profile, path in self.config.get("profiles", {}).items():
            self.profile_menu.add_radiobutton(
                label=f"{profile} ({path})",
                variable=self.profile_var,
                value=profile,
                command=self.switch_profile
            )
        self.profile_menu.add_separator()
        self.profile_menu.add_command(label="Добавить профиль", command=self.add_profile)
        self.profile_menu.add_command(label="Удалить профиль", command=self.delete_profile)

    def switch_profile(self):
        profile = self.profile_var.get()
        if profile in self.config["profiles"]:
            self.current_profile = profile
            self.notes_file = self.config["profiles"][profile]
            self.config["current_profile"] = profile
            self.save_config()
            self.notes_text.delete("1.0", tk.END)
            self.load_notes()
            messagebox.showinfo("Профиль", f"Активный профиль: {profile}\nФайл: {self.notes_file}")

    def add_profile(self):
        new_win = tk.Toplevel(self.root)
        new_win.title("Новый профиль")
        new_win.config(bg=self.theme.bg_color)
        new_win.geometry("400x150")

        tk.Label(new_win, text="Имя профиля:", bg=self.theme.bg_color, fg=self.theme.fg_color).pack(pady=5)
        name_var = tk.StringVar()
        name_entry = tk.Entry(new_win, textvariable=name_var, bg=self.theme.entry_bg, fg=self.theme.entry_fg)
        name_entry.pack(pady=5)

        def choose_file():
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                path_var.set(filename)

        tk.Label(new_win, text="Файл:", bg=self.theme.bg_color, fg=self.theme.fg_color).pack(pady=5)
        path_var = tk.StringVar(value="notes_new.txt")
        path_entry = tk.Entry(new_win, textvariable=path_var, width=40, bg=self.theme.entry_bg, fg=self.theme.entry_fg)
        path_entry.pack(pady=5)

        choose_btn = tk.Button(new_win, text="Выбрать...", command=choose_file, bg=self.theme.button_bg, fg=self.theme.button_fg)
        choose_btn.pack(pady=5)

        def save_new_profile():
            name = name_var.get().strip()
            path = path_var.get().strip()
            if not name:
                messagebox.showwarning("Ошибка", "Введите имя профиля")
                return
            if name in self.config["profiles"]:
                messagebox.showwarning("Ошибка", "Такой профиль уже существует")
                return
            self.config["profiles"][name] = path
            self.save_config()
            self.update_profile_menu()
            new_win.destroy()

        save_btn = tk.Button(new_win, text="Сохранить", command=save_new_profile,
                             bg=self.theme.button_bg, fg=self.theme.button_fg)
        save_btn.pack(pady=10)

    def delete_profile(self):
        profile = self.profile_var.get()
        if profile == "Default":
            messagebox.showwarning("Ошибка", "Нельзя удалить профиль по умолчанию")
            return
        if messagebox.askyesno("Удалить профиль", f"Удалить профиль '{profile}'?"):
            del self.config["profiles"][profile]
            self.current_profile = "Default"
            self.notes_file = self.config["profiles"]["Default"]
            self.profile_var.set("Default")
            self.save_config()
            self.update_profile_menu()
            self.switch_profile()

    def open_settings(self):
        messagebox.showinfo("Настройки", "Здесь будут общие настройки программы")

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить настройки:\n{e}")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {"profiles": {"Default": "notes.txt"}, "current_profile": "Default"}
        return {"profiles": {"Default": "notes.txt"}, "current_profile": "Default"}

    # ================== ВКЛАДКА ЗАДАЧИ ==================
    def create_task_widgets(self):
        self.task_entry = tk.Entry(
            self.task_frame,
            width=40,
            bg=self.theme.entry_bg,
            fg=self.theme.entry_fg,
            borderwidth=0
        )
        self.task_entry.pack(pady=5, padx=10)

        button_frame = tk.Frame(self.task_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=2)

        add_button = tk.Button(
            button_frame,
            text="Добавить",
            command=self.add_task,
            bg=self.theme.button_bg,
            fg=self.theme.button_fg,
            relief="flat"
        )
        add_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(
            button_frame,
            text="Удалить",
            command=self.delete_task,
            bg=self.theme.button_bg,
            fg=self.theme.button_fg,
            relief="flat"
        )
        delete_button.pack(side=tk.LEFT, padx=5)

        self.task_list = tk.Listbox(
            self.task_frame,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            selectbackground=self.theme.accent_color,
            selectforeground=self.theme.fg_color,
            borderwidth=0,
            highlightthickness=0
        )
        self.task_list.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            timestamp = datetime.now().strftime("%H:%M")
            formatted_task = f"{timestamp} - {task}"
            self.tasks.append(formatted_task)
            self.task_list.insert(tk.END, formatted_task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Предупреждение", "Введите задачу!")

    def delete_task(self):
        try:
            selected = self.task_list.curselection()
            self.task_list.delete(selected)
            self.tasks.pop(selected[0])
        except:
            messagebox.showwarning("Предупреждение", "Выберите задачу!")

    # ================== ВКЛАДКА КАРТЫ ==================
    def create_map_widgets(self):
        map_label = tk.Label(
            self.map_frame,
            text="Карты",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color
        )
        map_label.pack(pady=20)

    # ================== ВКЛАДКА ЗАМЕТКИ ==================
    def create_note_widgets(self):
        note_label = tk.Label(
            self.note_frame,
            text="Заметки",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=("Helvetica", 14, "bold")
        )
        note_label.pack(pady=10)

        self.notes_text = tk.Text(
            self.note_frame,
            bg=self.theme.entry_bg,
            fg=self.theme.entry_fg,
            wrap="word",
            height=15,
            width=60,
            borderwidth=0,
            highlightthickness=0
        )
        self.notes_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self.note_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=5)

        save_button = tk.Button(
            button_frame,
            text="Сохранить",
            command=self.save_notes,
            bg=self.theme.button_bg,
            fg=self.theme.button_fg,
            relief="flat"
        )
        save_button.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(
            button_frame,
            text="Очистить",
            command=self.clear_notes,
            bg=self.theme.button_bg,
            fg=self.theme.button_fg,
            relief="flat"
        )
        clear_button.pack(side=tk.LEFT, padx=5)

    def save_notes(self):
        text_data = self.notes_text.get("1.0", tk.END).strip()
        try:
            with open(self.notes_file, "w", encoding="utf-8") as f:
                f.write(text_data)
            messagebox.showinfo("Сохранение", f"Заметки сохранены в:\n{self.notes_file}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить заметки:\n{e}")

    def load_notes(self):
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, "r", encoding="utf-8") as f:
                    text_data = f.read()
                self.notes_text.insert("1.0", text_data)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить заметки:\n{e}")

    def clear_notes(self):
        self.notes_text.delete("1.0", tk.END)

    # ================== ВКЛАДКА НАВИГАТОР ==================
    def create_nav_widgets(self):
        nav_label = tk.Label(
            self.nav_frame,
            text="Навигатор",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=("Helvetica", 14, "bold")
        )
        nav_label.pack(pady=20)

        self.coords_entry = tk.Entry(
            self.nav_frame,
            width=40,
            bg=self.theme.entry_bg,
            fg=self.theme.entry_fg,
            borderwidth=0
        )
        self.coords_entry.pack(pady=5, padx=10)

        search_button = tk.Button(
            self.nav_frame,
            text="Найти маршрут",
            command=self.search_route,
            bg=self.theme.button_bg,
            fg=self.theme.button_fg,
            relief="flat"
        )
        search_button.pack(pady=2)

        self.route_text = tk.Text(
            self.nav_frame,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            borderwidth=0,
            highlightthickness=0,
            height=15,
            width=50
        )
        self.route_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def search_route(self):
        coords = self.coords_entry.get()
        if coords:
            self.route_text.delete(1.0, tk.END)
            self.route_text.insert(tk.END, f"Поиск маршрута до: {coords}\n")
            self.route_text.insert(tk.END, "Пример маршрута:\n")
            self.route_text.insert(tk.END, "1. Поверните направо\n")
            self.route_text.insert(tk.END, "2. Проедьте 2 км\n")
            self.coords_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Предупреждение", "Введите координаты!")


def main():
    root = tk.Tk()
    app = MultiTabApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
