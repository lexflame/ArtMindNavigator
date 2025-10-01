import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import json
import os

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

class MultiTabApp:
    def __init__(self, root):
        self.root = root
        self.theme = DarkTheme()
        self.tasks = []
        self.autosave_file = "tasks.json"

        # Убираем стандартный заголовок и разворачиваем
        self.root.overrideredirect(True)
        self.root.state("zoomed")
        self.root.config(bg=self.theme.bg_color)
        self.is_maximized = True
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # ===== КАСТОМНЫЙ ЗАГОЛОВОК =====
        self.title_bar = tk.Frame(self.root, bg=self.theme.title_bar_bg, height=40)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)

        self.title_label = tk.Label(self.title_bar, text="MindNavigator",
                                    bg=self.theme.title_bar_bg, fg=self.theme.fg_color,
                                    font=("Helvetica", 12, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=5)

        # ===== Закладки =====
        self.bookmark_frame = tk.Frame(self.title_bar, bg=self.theme.title_bar_bg)
        self.bookmark_frame.pack(side=tk.LEFT, padx=20)

        self.bookmarks = {
            "Задачи": self.show_tasks,
            "Карты": self.show_maps,
            "Заметки": self.show_notes,
            "Навигатор": self.show_nav
        }

        for name, cmd in self.bookmarks.items():
            btn = tk.Button(self.bookmark_frame, text=name, command=cmd,
                            bg=self.theme.button_bg, fg=self.theme.button_fg,
                            relief="flat", padx=10, pady=3)
            btn.pack(side=tk.LEFT, padx=5)

        # ===== Кнопки управления окном =====
        self.btn_min = tk.Button(self.title_bar, text="━", command=self.minimize,
                                 bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", width=4)
        self.btn_min.pack(side=tk.RIGHT, padx=2)

        self.btn_max = tk.Button(self.title_bar, text="❐", command=self.toggle_maximize,
                                 bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", width=4)
        self.btn_max.pack(side=tk.RIGHT, padx=2)

        self.btn_close = tk.Button(self.title_bar, text="✕", command=self.on_close,
                                   bg="#FF5555", fg="white", relief="flat", width=4)
        self.btn_close.pack(side=tk.RIGHT, padx=2)

        # ===== Контент =====
        self.content = tk.Frame(self.root, bg=self.theme.bg_color)
        self.content.pack(fill=tk.BOTH, expand=True)

        self.task_frame = tk.Frame(self.content, bg=self.theme.bg_color)
        self.map_frame = tk.Frame(self.content, bg=self.theme.bg_color)
        self.note_frame = tk.Frame(self.content, bg=self.theme.bg_color)
        self.nav_frame = tk.Frame(self.content, bg=self.theme.bg_color)

        # ===== Инициализация вкладок =====
        self.show_tasks()
        self.create_task_widgets()
        self.create_map_widgets()
        self.create_note_widgets()
        self.create_nav_widgets()

        # ===== Перемещение окна =====
        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.on_move)
        self.title_bar.bind("<Double-Button-1>", lambda e: self.toggle_maximize())

        # ===== Автозагрузка задач =====
        if os.path.exists(self.autosave_file):
            try:
                with open(self.autosave_file, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
                self.refresh_task_list()
            except:
                self.tasks = []

    # ===== Окно =====
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

    # ===== Навигация =====
    def show_frame(self, frame):
        for f in [self.task_frame, self.map_frame, self.note_frame, self.nav_frame]:
            f.pack_forget()
        frame.pack(fill=tk.BOTH, expand=True)

    def show_tasks(self): self.show_frame(self.task_frame)
    def show_maps(self): self.show_frame(self.map_frame)
    def show_notes(self): self.show_frame(self.note_frame)
    def show_nav(self): self.show_frame(self.nav_frame)

    # ===== Задачи =====
    def create_task_widgets(self):
        input_frame = tk.Frame(self.task_frame, bg=self.theme.bg_color)
        input_frame.pack(pady=5, padx=10, fill=tk.X)

        self.task_entry = tk.Entry(input_frame, width=20, bg=self.theme.entry_bg, fg=self.theme.entry_fg, borderwidth=0)
        self.task_entry.pack(side=tk.LEFT, padx=2)

        self.desc_entry = tk.Entry(input_frame, width=25, bg=self.theme.entry_bg, fg=self.theme.entry_fg, borderwidth=0)
        self.desc_entry.pack(side=tk.LEFT, padx=2)

        self.date_entry = DateEntry(input_frame, width=12, background='darkblue', foreground='white', borderwidth=1, date_pattern='dd.mm.yyyy')
        self.date_entry.pack(side=tk.LEFT, padx=2)

        self.hour_var = tk.StringVar(value="12")
        self.minute_var = tk.StringVar(value="00")
        self.hour_cb = ttk.Combobox(input_frame, width=3, textvariable=self.hour_var, values=[f"{i:02d}" for i in range(24)], state="readonly")
        self.hour_cb.pack(side=tk.LEFT)
        self.minute_cb = ttk.Combobox(input_frame, width=3, textvariable=self.minute_var, values=[f"{i:02d}" for i in range(60)], state="readonly")
        self.minute_cb.pack(side=tk.LEFT)

        self.priority_var = tk.StringVar(value="Средний")
        self.priority_menu = ttk.Combobox(input_frame, textvariable=self.priority_var, values=["Низкий","Средний","Высокий"], state="readonly", width=10)
        self.priority_menu.pack(side=tk.LEFT, padx=2)

        add_btn = tk.Button(input_frame, text="Добавить", command=self.add_task, bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat")
        add_btn.pack(side=tk.LEFT, padx=2)

        self.task_list = tk.Listbox(self.task_frame, bg=self.theme.bg_color, fg=self.theme.fg_color,
                                    selectbackground=self.theme.accent_color, selectforeground=self.theme.fg_color,
                                    borderwidth=0, highlightthickness=0, width=120, height=15)
        self.task_list.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        self.task_list.bind("<<ListboxSelect>>", self.on_task_select)

        btn_frame = tk.Frame(self.task_frame, bg=self.theme.bg_color)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Обновить", command=self.update_task,
                  bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_task,
                  bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", width=12).pack(side=tk.LEFT, padx=5)

    def add_task(self):
        task = self.task_entry.get().strip()
        desc = self.desc_entry.get().strip()
        date = self.date_entry.get_date().strftime("%d.%m.%Y")
        time = f"{self.hour_var.get()}:{self.minute_var.get()}"
        due = f"{date} {time}"
        priority = self.priority_var.get()

        if not task:
            messagebox.showwarning("Предупреждение", "Введите название задачи!")
            return

        display_text = f"[{priority}] {task} - {desc} (Срок: {due})" if desc else f"[{priority}] {task} (Срок: {due})"
        self.tasks.append({"task": task, "desc": desc, "due": due, "priority": priority})
        self.refresh_task_list()
        self.clear_form()

    def on_task_select(self, event):
        try:
            index = self.task_list.curselection()[0]
            t = self.tasks[index]
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, t["task"])
            self.desc_entry.delete(0, tk.END)
            self.desc_entry.insert(0, t["desc"])
            self.date_entry.set_date(datetime.strptime(t["due"].split()[0], "%d.%m.%Y"))
            self.hour_var.set(t["due"].split()[1].split(":")[0])
            self.minute_var.set(t["due"].split()[1].split(":")[1])
            self.priority_var.set(t["priority"])
        except IndexError:
            pass

    def update_task(self):
        try:
            index = self.task_list.curselection()[0]
            task = self.task_entry.get().strip()
            desc = self.desc_entry.get().strip()
            date = self.date_entry.get_date().strftime("%d.%m.%Y")
            time = f"{self.hour_var.get()}:{self.minute_var.get()}"
            due = f"{date} {time}"
            priority = self.priority_var.get()
            if not task:
                messagebox.showwarning("Предупреждение", "Введите название задачи!")
                return
            self.tasks[index] = {"task": task, "desc": desc, "due": due, "priority": priority}
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Предупреждение", "Выберите задачу!")

    def delete_task(self):
        try:
            index = self.task_list.curselection()[0]
            self.tasks.pop(index)
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Предупреждение", "Выберите задачу!")

    def refresh_task_list(self):
        self.task_list.delete(0, tk.END)
        for t in self.tasks:
            display_text = f"[{t['priority']}] {t['task']} - {t['desc']} (Срок: {t['due']})" if t['desc'] else f"[{t['priority']}] {t['task']} (Срок: {t['due']})"
            self.task_list.insert(tk.END, display_text)

    def clear_form(self):
        self.task_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.date_entry.set_date(datetime.now())
        self.hour_var.set("12")
        self.minute_var.set("00")
        self.priority_var.set("Средний")

    def on_close(self):
        try:
            with open(self.autosave_file, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except:
            pass
        self.root.destroy()

    # ===== Остальные вкладки =====
    def create_map_widgets(self):
        tk.Label(self.map_frame, text="Карты", bg=self.theme.bg_color, fg=self.theme.fg_color).pack(pady=20)

    def create_note_widgets(self):
        tk.Label(self.note_frame, text="Заметки (в разработке)", bg=self.theme.bg_color, fg=self.theme.fg_color).pack(pady=20)

    def create_nav_widgets(self):
        tk.Label(self.nav_frame, text="Навигатор", bg=self.theme.bg_color, fg=self.theme.fg_color,
                 font=("Helvetica", 14, "bold")).pack(pady=20)


def main():
    root = tk.Tk()
    app = MultiTabApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
