import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
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
        self.tab_bg = "#36393F"  # Цвет фона вкладок
        self.tab_fg = "#FFFFFF"  # Цвет текста вкладок
        self.tab_selected_bg = "#444850"  # Цвет активной вкладки
        self.tab_selected_fg = "#FFFFFF"  # Цвет текста активной вкладки


class MultiTabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MindNavigator")
        self.root.config(bg=DarkTheme().bg_color)
        self.tasks = []

        # Создание Notebook (вкладок)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill=tk.BOTH)

        self.theme = DarkTheme()
        # root.overrideredirect(True)

        # Настройка стилей ttk для темной темы
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

        # Остальной код остается прежним...

        # Создаем кастомную панель заголовка
        self.title_bar = tk.Frame(root, bg=self.theme.title_bar_bg, height=30)
        self.title_bar.pack(fill=tk.X)

        # Основной контент приложения
        self.content = tk.Frame(root, bg=self.theme.bg_color)
        self.content.pack(fill=tk.BOTH, expand=True)

        # Создание фреймов для каждой вкладки
        self.task_frame = tk.Frame(self.notebook, bg=DarkTheme().bg_color)
        self.map_frame = tk.Frame(self.notebook, bg=DarkTheme().bg_color)
        self.note_frame = tk.Frame(self.notebook, bg=DarkTheme().bg_color)
        self.nav_frame = tk.Frame(self.notebook, bg=DarkTheme().bg_color)

        # Добавление вкладок
        self.notebook.add(self.task_frame, text="Задачи")
        self.notebook.add(self.map_frame, text="Карты")
        self.notebook.add(self.note_frame, text="Заметки")
        self.notebook.add(self.nav_frame, text="Навигатор")

        # Настройка виджетов для каждой вкладки
        self.create_task_widgets()
        self.create_map_widgets()
        self.create_note_widgets()
        self.create_nav_widgets()

    def create_nav_widgets(self):
        # Заголовок вкладки
        nav_label = tk.Label(
            self.nav_frame,
            text="Навигатор",
            bg=DarkTheme().bg_color,
            fg=DarkTheme().fg_color,
            font=("Helvetica", 14, "bold")
        )
        nav_label.pack(pady=20)

        # Поле ввода координат
        self.coords_entry = tk.Entry(
            self.nav_frame,
            width=40,
            bg=DarkTheme().entry_bg,
            fg=DarkTheme().entry_fg,
            borderwidth=0
        )
        self.coords_entry.pack(pady=5, padx=10)

        # Кнопка поиска маршрута
        search_button = tk.Button(
            self.nav_frame,
            text="Найти маршрут",
            command=self.search_route,
            bg=DarkTheme().button_bg,
            fg=DarkTheme().button_fg,
            relief="flat"
        )
        search_button.pack(pady=2)

        # Текстовое поле для отображения маршрута
        self.route_text = tk.Text(
            self.nav_frame,
            bg=DarkTheme().bg_color,
            fg=DarkTheme().fg_color,
            borderwidth=0,
            highlightthickness=0,
            height=15,
            width=50
        )
        self.route_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def search_route(self):
        # Временная реализация
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

    def create_task_widgets(self):
        # Поле ввода задачи
        self.task_entry = tk.Entry(
            self.task_frame,
            width=40,
            bg=DarkTheme().entry_bg,
            fg=DarkTheme().entry_fg,
            borderwidth=0
        )
        self.task_entry.pack(pady=5, padx=10)

        # Кнопка добавления
        add_button = tk.Button(
            self.task_frame,
            text="Добавить",
            command=self.add_task,
            bg=DarkTheme().button_bg,
            fg=DarkTheme().button_fg,
            relief="flat"
        )
        add_button.pack(pady=2)

        # Список задач
        self.task_list = tk.Listbox(
            self.root,
            bg=DarkTheme().bg_color,
            fg=DarkTheme().fg_color,
            selectbackground=DarkTheme().accent_color,
            selectforeground=DarkTheme().fg_color,
            borderwidth=0,
            highlightthickness=0
        )
        self.task_list.pack(pady=20, padx=10, fill=tk.BOTH, expand=False)

    def create_map_widgets(self):
        map_label = tk.Label(
            self.map_frame,
            text="Карты",
            bg=DarkTheme().bg_color,
            fg=DarkTheme().fg_color
        )
        map_label.pack(pady=20)

        # Здесь можно добавить виджеты для работы с картами
    def create_note_widgets(self):
        note_label = tk.Label(
            self.note_frame,
            text="Заметки",
            bg=DarkTheme().bg_color,
            fg=DarkTheme().fg_color
        )

def main():
    root = tk.Tk()
    app = MultiTabApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()