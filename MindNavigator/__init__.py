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
        self.title_bar_bg = "#202225"
        self.tab_bg = "#36393F"
        self.tab_fg = "#FFFFFF"
        self.tab_selected_bg = "#444850"
        self.tab_selected_fg = "#FFFFFF"


class MultiTabApp:
    def __init__(self, root):
        self.root = root
        self.theme = DarkTheme()

        # Иконка для панели задач
        try:
            self.root.iconbitmap("icon.ico")  # .ico файл
        except:
            pass  # если файла нет, просто пропускаем

        # Убираем стандартный заголовок и разворачиваем
        self.root.overrideredirect(True)
        self.root.state("zoomed")
        self.root.config(bg=self.theme.bg_color)

        self.is_maximized = True
        self.tasks = []

        # ==== КАСТОМНЫЙ ЗАГОЛОВОК ====
        self.title_bar = tk.Frame(self.root, bg=self.theme.title_bar_bg, relief="flat", height=40)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)

        # Иконка в заголовке
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")  # маленькая PNG иконка
            self.icon_label = tk.Label(
                self.title_bar,
                image=self.icon_img,
                bg=self.theme.title_bar_bg
            )
            self.icon_label.pack(side=tk.LEFT, padx=5)
        except:
            pass  # если файла нет, просто пропускаем

        # Название приложения
        self.title_label = tk.Label(
            self.title_bar,
            text="MindNavigator",
            bg=self.theme.title_bar_bg,
            fg=self.theme.fg_color,
            font=("Helvetica", 12, "bold")
        )
        self.title_label.pack(side=tk.LEFT, padx=5)

        # ==== ЗАКЛАДКИ ====
        self.bookmark_frame = tk.Frame(self.title_bar, bg=self.theme.title_bar_bg)
        self.bookmark_frame.pack(side=tk.LEFT, padx=20)

        self.bookmarks = {
            "Задачи": self.show_tasks,
            "Карты": self.show_maps,
            "Заметки": self.show_notes,
            "Навигатор": self.show_nav
        }

        for name, cmd in self.bookmarks.items():
            btn = tk.Button(
                self.bookmark_frame,
                text=name,
                command=cmd,
                bg=self.theme.button_bg,
                fg=self.theme.button_fg,
                relief="flat",
                padx=10, pady=3
            )
            btn.pack(side=tk.LEFT, padx=5)

        # ==== Кнопки управления окном ====
        self.btn_close = tk.Button(
            self.title_bar, text="✕", command=self.root.quit,
            bg="#FF5555", fg="white", relief="flat", width=4
        )
        self.btn_close.pack(side=tk.RIGHT, padx=2)


        self.btn_max = tk.Button(
            self.title_bar, text="❐", command=self.toggle_maximize,
            bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", width=4
        )
        self.btn_max.pack(side=tk.RIGHT, padx=2)

        self.btn_min = tk.Button(
            self.title_bar, text="━", command=self.minimize,
            bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", width=4
        )
        self.btn_min.pack(side=tk.RIGHT, padx=2)



        # ==== ОСНОВНОЙ КОНТЕНТ ====
        self.content = tk.Frame(self.root, bg=self.theme.bg_color)
        self.content.pack(fill=tk.BOTH, expand=True)

        # Фреймы вместо Notebook
        self.task_frame = tk.Frame(self.content, bg=self.theme.bg_color)
        self.map_frame = tk.Frame(self.content, bg=self.theme.bg_color)
        self.note_frame = tk.Frame(self.content, bg=self.theme.bg_color)
        self.nav_frame = tk.Frame(self.content, bg=self.theme.bg_color)

        # Изначально показываем задачи
        self.show_tasks()

        # Создаем виджеты
        self.create_task_widgets()
        self.create_map_widgets()
        self.create_note_widgets()
        self.create_nav_widgets()

        # ==== ДВИЖЕНИЕ ОКНА ====
        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.on_move)

        # ==== Двойной клик по заголовку для разворота/восстановления ====
        self.title_bar.bind("<Double-Button-1>", lambda e: self.toggle_maximize())

    # ===== Методы управления окна =====
    def minimize(self):
        self.root.overrideredirect(False)
        self.root.iconify()

    def toggle_maximize(self):
        if self.is_maximized:
            self.root.state("normal")
            self.is_maximized = False
        else:
            self.root.state("zoomed")
            self.is_maximized = True
        self.root.overrideredirect(True)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    # ===== Навигация между фреймами =====
    def show_frame(self, frame):
        for f in [self.task_frame, self.map_frame, self.note_frame, self.nav_frame]:
            f.pack_forget()
        frame.pack(fill=tk.BOTH, expand=True)

    def show_tasks(self):
        self.show_frame(self.task_frame)

    def show_maps(self):
        self.show_frame(self.map_frame)

    def show_notes(self):
        self.show_frame(self.note_frame)

    def show_nav(self):
        self.show_frame(self.nav_frame)

    # ===== Виджеты =====
    def create_task_widgets(self):
        self.task_entry = tk.Entry(
            self.task_frame,
            width=40,
            bg=self.theme.entry_bg,
            fg=self.theme.entry_fg,
            borderwidth=0
        )
        self.task_entry.pack(pady=5, padx=10)

        add_button = tk.Button(
            self.task_frame, text="Добавить", command=self.add_task,
            bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat"
        )
        add_button.pack(pady=2)

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

    def create_map_widgets(self):
        map_label = tk.Label(
            self.map_frame,
            text="Карты",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color
        )
        map_label.pack(pady=20)

    def create_note_widgets(self):
        note_label = tk.Label(
            self.note_frame,
            text="Заметки (в разработке)",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color
        )
        note_label.pack(pady=20)

    def create_nav_widgets(self):
        nav_label = tk.Label(
            self.nav_frame,
            text="Навигатор",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=("Helvetica", 14, "bold")
        )
        nav_label.pack(pady=20)

    # ===== Логика задач =====
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


def main():
    root = tk.Tk()
    app = MultiTabApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
