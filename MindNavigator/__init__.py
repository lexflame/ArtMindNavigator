import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class DarkTheme:
    def __init__(self):
        self.bg_color = "#2C2F33"
        self.fg_color = "#FFFFFF"
        self.accent_color = "#7289DA"
        self.entry_bg = "#36393F"
        self.entry_fg = "#FFFFFF"
        self.button_bg = "#23272A"
        self.button_fg = "#FFFFFF"
        self.title_bar_bg = "#333333"
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
        self.notes_file = "notes.txt"

        # --- Кастомная панель заголовка ---
        self.title_bar = tk.Frame(root, bg=self.theme.title_bar_bg, height=40)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)

        # Название приложения слева
        self.app_title = tk.Label(
            self.title_bar,
            text="MindNavigator",
            bg=self.theme.title_bar_bg,
            fg=self.theme.fg_color,
            font=("Helvetica", 12, "bold")
        )
        self.app_title.pack(side=tk.LEFT, padx=10)

        # --- Встроенный Notebook (закладки) в заголовок ---
        self.notebook = ttk.Notebook(self.title_bar)
        self.notebook.pack(side=tk.LEFT, padx=20, pady=2, expand=True, fill=tk.X)

        # Стилизация вкладок
        self.style = ttk.Style()
        self.style.theme_create("DarkStyle", parent="alt", settings={
            "TNotebook": {
                "configure": {"background": self.theme.title_bar_bg, "tabmargins": [2, 2, 2, 0]},
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

        # --- Основной контент (область под заголовком) ---
        self.content = tk.Frame(root, bg=self.theme.bg_color)
        self.content.pack(fill=tk.BOTH, expand=True)

        # Фреймы для вкладок (содержимое)
        self.task_frame = tk.Frame(self.content, bg=self.theme.bg_color)
        self.map_frame = tk.Frame(self.content, bg=self.theme.bg_color)
        self.note_frame = tk.Frame(self.content, bg=self.theme.bg_color)
        self.nav_frame = tk.Frame(self.content, bg=self.theme.bg_color)

        # Привязка вкладок к фреймам
        self.notebook.add(self.task_frame, text="Задачи")
        self.notebook.add(self.map_frame, text="Карты")
        self.notebook.add(self.note_frame, text="Заметки")
        self.notebook.add(self.nav_frame, text="Навигатор")

        # Создание виджетов
        self.create_task_widgets()
        self.create_map_widgets()
        self.create_note_widgets()
        self.create_nav_widgets()

    # ---------------- Вкладка Навигатор ----------------
    def create_nav_widgets(self):
        nav_label = tk.Label(
            self.nav_frame, text="Навигатор",
            bg=self.theme.bg_color, fg=self.theme.fg_color,
            font=("Helvetica", 14, "bold")
        )
        nav_label.pack(pady=20)

        self.coords_entry = tk.Entry(
            self.nav_frame, width=40,
            bg=self.theme.entry_bg, fg=self.theme.entry_fg, borderwidth=0
        )
        self.coords_entry.pack(pady=5, padx=10)

        search_button = tk.Button(
            self.nav_frame, text="Найти маршрут",
            command=self.search_route,
            bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat"
        )
        search_button.pack(pady=2)

        self.route_text = tk.Text(
            self.nav_frame, bg=self.theme.bg_color, fg=self.theme.fg_color,
            borderwidth=0, highlightthickness=0, height=15, width=50
        )
        self.route_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def search_route(self):
        coords = self.coords_entry.get()
        if coords:
            self.route_text.delete(1.0, tk.END)
            self.route_text.insert(tk.END, f"Поиск маршрута до: {coords}\n")
            self.route_text.insert(tk.END, "Пример маршрута:\n")
            self.route_text.insert(tk.END, "1. Поверните направо\n2. Проедьте 2 км\n")
            self.coords_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Предупреждение", "Введите координаты!")

    # ---------------- Вкладка Задачи ----------------
    def create_task_widgets(self):
        self.task_entry = tk.Entry(
            self.task_frame, width=40,
            bg=self.theme.entry_bg, fg=self.theme.entry_fg, borderwidth=0
        )
        self.task_entry.pack(pady=5, padx=10)

        add_button = tk.Button(
            self.task_frame, text="Добавить", command=self.add_task,
            bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat"
        )
        add_button.pack(pady=2)

        delete_button = tk.Button(
            self.task_frame, text="Удалить", command=self.delete_task,
            bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat"
        )
        delete_button.pack(pady=2)

        self.task_list = tk.Listbox(
            self.task_frame,
            bg=self.theme.bg_color, fg=self.theme.fg_color,
            selectbackground=self.theme.accent_color,
            selectforeground=self.theme.fg_color,
            borderwidth=0, highlightthickness=0
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

    # ---------------- Вкладка Карты ----------------
    def create_map_widgets(self):
        map_label = tk.Label(
            self.map_frame, text="Карты",
            bg=self.theme.bg_color, fg=self.theme.fg_color
        )
        map_label.pack(pady=20)

    # ---------------- Вкладка Заметки ----------------
    def create_note_widgets(self):
        note_label = tk.Label(
            self.note_frame, text="Заметки",
            bg=self.theme.bg_color, fg=self.theme.fg_color
        )
        note_label.pack(pady=5)

        self.note_text = tk.Text(
            self.note_frame, wrap=tk.WORD,
            bg=self.theme.entry_bg, fg=self.theme.entry_fg,
            borderwidth=0, highlightthickness=0
        )
        self.note_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        save_button = tk.Button(
            self.note_frame, text="Сохранить заметки",
            command=self.save_notes,
            bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat"
        )
        save_button.pack(pady=5)

        self.load_notes()

    def save_notes(self):
        with open(self.notes_file, "w", encoding="utf-8") as f:
            f.write(self.note_text.get(1.0, tk.END))

    def load_notes(self):
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                self.note_text.insert(tk.END, f.read())
        except FileNotFoundError:
            pass


def main():
    root = tk.Tk()
    app = MultiTabApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
