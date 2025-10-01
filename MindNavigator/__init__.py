import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
        self.completed_tasks = []
        self.autosave_file = "tasks.json"

        # ===== Настройка окна =====
        self.root.overrideredirect(True)
        self.root.state("zoomed")
        self.root.config(bg=self.theme.bg_color)
        self.is_maximized = True
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # ===== Кастомный заголовок =====
        self.title_bar = tk.Frame(self.root, bg=self.theme.title_bar_bg, height=40)
        self.title_bar.pack(fill=tk.X)
        self.title_label = tk.Label(self.title_bar, text="MindNavigator",
                                    bg=self.theme.title_bar_bg, fg=self.theme.fg_color,
                                    font=("Helvetica", 12, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=5)
        self.btn_min = tk.Button(self.title_bar, text="━", command=self.minimize,
                                 bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", width=4)
        self.btn_min.pack(side=tk.RIGHT, padx=2)
        self.btn_max = tk.Button(self.title_bar, text="❐", command=self.toggle_maximize,
                                 bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", width=4)
        self.btn_max.pack(side=tk.RIGHT, padx=2)
        self.btn_close = tk.Button(self.title_bar, text="✕", command=self.on_close,
                                   bg="#FF5555", fg="white", relief="flat", width=4)
        self.btn_close.pack(side=tk.RIGHT, padx=2)
        self.btn_settings = tk.Button(self.title_bar, text="⚙", command=self.select_file_paths,
                                      bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", width=4)
        self.btn_settings.pack(side=tk.RIGHT, padx=2)

        # ===== Панель закладок =====
        self.bookmark_toolbar = tk.Frame(self.root, bg=self.theme.title_bar_bg, height=40)
        self.bookmark_toolbar.pack(fill=tk.X)
        self.bookmarks = {"Задачи": self.show_tasks, "Карты": self.show_maps,
                          "Заметки": self.show_notes, "Навигатор": self.show_nav}
        self.bookmark_icons = {"Задачи": "📝","Карты": "🗺️","Заметки": "📓","Навигатор": "🧭"}
        for name, icon in self.bookmark_icons.items():
            btn = tk.Button(self.bookmark_toolbar, text=f"{icon} {name}", command=self.bookmarks[name],
                            bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", padx=10, pady=5)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # ===== Контент =====
        self.content = tk.Frame(self.root, bg=self.theme.bg_color)
        self.content.pack(fill=tk.BOTH, expand=True)
        self.task_frame = tk.Frame(self.content, bg=self.theme.bg_color)
        self.map_frame = tk.Frame(self.content, bg=self.theme.bg_color)
        self.note_frame = tk.Frame(self.content, bg=self.theme.bg_color)
        self.nav_frame = tk.Frame(self.content, bg=self.theme.bg_color)

        self.show_tasks()
        self.create_task_widgets()
        self.create_map_widgets()
        self.create_note_widgets()
        self.create_nav_widgets()

        # ===== Перемещение окна =====
        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.on_move)
        self.title_bar.bind("<Double-Button-1>", lambda e: self.toggle_maximize())

        # ===== Автозагрузка данных =====
        if os.path.exists(self.autosave_file):
            try:
                with open(self.autosave_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])
                    self.completed_tasks = data.get("completed", [])
            except:
                self.tasks = []
                self.completed_tasks = []

        self.task_list_frame = tk.Frame(self.task_frame, bg=self.theme.bg_color)
        self.task_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

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

    # ===== Настройка файлов =====
    def select_file_paths(self):
        notes_file = filedialog.asksaveasfilename(title="Выберите файл для заметок",
                                                  defaultextension=".txt",
                                                  filetypes=[("Text files","*.txt")])
        if notes_file: self.notes_file = notes_file

        maps_file = filedialog.asksaveasfilename(title="Выберите файл для карт",
                                                 defaultextension=".txt",
                                                 filetypes=[("Text files","*.txt")])
        if maps_file: self.maps_file = maps_file

        tasks_file = filedialog.asksaveasfilename(title="Выберите файл для задач",
                                                  defaultextension=".json",
                                                  filetypes=[("JSON files","*.json")])
        if tasks_file: self.autosave_file = tasks_file

        messagebox.showinfo("Настройки", "Файлы успешно выбраны!")

    # ===== Задачи =====
    def create_task_widgets(self):
        input_frame = tk.Frame(self.task_frame, bg=self.theme.bg_color)
        input_frame.pack(fill=tk.X, pady=5, padx=10)

        self.task_entry = tk.Entry(input_frame, bg=self.theme.entry_bg, fg=self.theme.entry_fg)
        self.task_entry.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        self.desc_entry = tk.Entry(input_frame, bg=self.theme.entry_bg, fg=self.theme.entry_fg)
        self.desc_entry.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
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

        # ===== Фильтр =====
        self.filter_var = tk.StringVar(value="Все")
        filter_frame = tk.Frame(self.task_frame, bg=self.theme.bg_color)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(filter_frame, text="Фильтр:", background=self.theme.bg_color, foreground=self.theme.fg_color).pack(side=tk.LEFT)
        filter_menu = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=["Все","Высокий","Средний","Низкий","Важные"], state="readonly", width=10)
        filter_menu.pack(side=tk.LEFT, padx=5)
        filter_menu.bind("<<ComboboxSelected>>", lambda e: self.refresh_task_list())

        # ===== Показывать выполненные =====
        self.show_done_var = tk.BooleanVar(value=False)
        show_done_cb = tk.Checkbutton(filter_frame, text="Показывать выполненные",
                                      variable=self.show_done_var, bg=self.theme.bg_color,
                                      fg=self.theme.fg_color, command=self.refresh_task_list)
        show_done_cb.pack(side=tk.LEFT, padx=10)

        # ===== Архив выполненных =====
        archive_btn = tk.Button(filter_frame, text="Архив выполненных",
                                bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat",
                                command=self.show_archive)
        archive_btn.pack(side=tk.LEFT, padx=5)

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
        self.tasks.append({"task": task, "desc": desc, "due": due, "priority": priority, "done": False, "important": False})
        self.refresh_task_list()
        self.clear_task_form()

    def refresh_task_list(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        now = datetime.now()
        f = self.filter_var.get()
        for t in self.tasks:
            if t.get("done", False) and not self.show_done_var.get():
                continue
            if f == "Важные" and not t.get("important", False):
                continue
            elif f in ["Высокий","Средний","Низкий"] and t["priority"] != f:
                continue

            due_dt = datetime.strptime(t["due"], "%d.%m.%Y %H:%M")
            bg_color = {"Высокий":"#F04747","Средний":"#FAA61A","Низкий":"#43B581"}.get(t["priority"], self.theme.entry_bg)
            if not t.get("done", False) and due_dt < now:
                bg_color = "#8B0000"

            frame = tk.Frame(self.task_list_frame, bg=bg_color, bd=1, relief="solid")
            frame.pack(fill=tk.X, padx=5, pady=3)
            frame.index = self.tasks.index(t)

            var = tk.BooleanVar(value=t.get("done", False))
            chk = tk.Checkbutton(frame, variable=var, bg=bg_color,
                                 command=lambda i=frame.index,v=var: self.toggle_done(i,v))
            chk.pack(side=tk.LEFT, padx=5)

            star_btn = tk.Button(frame, text="★" if t.get("important", False) else "☆",
                                 bg=bg_color, fg="#FFD700", relief="flat",
                                 command=lambda i=frame.index: self.toggle_important(i))
            star_btn.pack(side=tk.LEFT, padx=5)

            fg_color = self.theme.fg_color if not t.get("done", False) else "#888888"
            task_text = t["task"]
            if t.get("done", False):
                task_text = f"✔ {task_text}"
            tk.Label(frame, text=task_text, bg=bg_color, fg=fg_color, font=("Helvetica",12,"bold")).pack(side=tk.TOP, anchor="w")
            if t["desc"]:
                tk.Label(frame, text=t["desc"], bg=bg_color, fg=self.theme.fg_color, font=("Helvetica",10)).pack(side=tk.TOP, anchor="w")
            tk.Label(frame, text=t["due"], bg=bg_color, fg="#FFFFFF", font=("Helvetica",9)).pack(side=tk.RIGHT, padx=5)
            self.make_draggable(frame)
        self.autosave_tasks()

    def toggle_done(self,index,var):
        task = self.tasks[index]
        task["done"] = var.get()
        if var.get():  # перемещаем в архив
            self.completed_tasks.append(task)
            self.tasks.pop(index)
        self.refresh_task_list()

    def toggle_important(self,index):
        self.tasks[index]["important"] = not self.tasks[index].get("important", False)
        self.refresh_task_list()

    def clear_task_form(self):
        self.task_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.date_entry.set_date(datetime.now())
        self.hour_var.set("12")
        self.minute_var.set("00")
        self.priority_var.set("Средний")

    def autosave_tasks(self):
        try:
            with open(self.autosave_file, "w", encoding="utf-8") as f:
                json.dump({"tasks": self.tasks, "completed": self.completed_tasks}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("Ошибка автосохранения:", e)

    # ===== Drag&Drop =====
    def make_draggable(self, widget):
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)
        widget.bind("<ButtonRelease-1>", self.on_drag_release)

    def on_drag_start(self, event):
        self.drag_data = {"widget": event.widget, "y": event.y_root}

    def on_drag_motion(self, event):
        widget = self.drag_data["widget"]
        dy = event.y_root - self.drag_data["y"]
        widget.place(y=widget.winfo_y() + dy)
        self.drag_data["y"] = event.y_root

    def on_drag_release(self, event):
        widget = self.drag_data["widget"]
        widget.place_forget()
        children = sorted(self.task_list_frame.winfo_children(), key=lambda w: w.winfo_y())
        new_tasks_order = []
        for w in children:
            new_tasks_order.append(self.tasks[w.index])
        self.tasks = new_tasks_order
        self.refresh_task_list()
        self.drag_data = None

    def show_archive(self):
        archive_win = tk.Toplevel(self.root)
        archive_win.title("Архив выполненных задач")
        archive_win.geometry("600x400")
        archive_win.config(bg=self.theme.bg_color)

        list_frame = tk.Frame(archive_win, bg=self.theme.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for t in self.completed_tasks:
            due_dt = t["due"]
            bg_color = {"Высокий":"#F04747","Средний":"#FAA61A","Низкий":"#43B581"}.get(t["priority"], self.theme.entry_bg)
            frame = tk.Frame(list_frame, bg=bg_color, bd=1, relief="solid")
            frame.pack(fill=tk.X, padx=5, pady=3)
            tk.Label(frame, text=f"✔ {t['task']} ({due_dt})", bg=bg_color, fg="#888888", font=("Helvetica",12,"bold")).pack(side=tk.LEFT)
            if t["desc"]:
                tk.Label(frame, text=t["desc"], bg=bg_color, fg="#CCCCCC", font=("Helvetica",10)).pack(side=tk.LEFT)

    # ===== Заметки =====
    def create_note_widgets(self):
        self.note_text = tk.Text(self.note_frame, bg=self.theme.bg_color, fg=self.theme.fg_color)
        self.note_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ===== Навигатор =====
    def create_nav_widgets(self):
        tk.Label(self.nav_frame, text="Навигатор", bg=self.theme.bg_color, fg=self.theme.fg_color).pack(pady=10)
        self.coords_entry = tk.Entry(self.nav_frame, bg=self.theme.entry_bg, fg=self.theme.entry_fg)
        self.coords_entry.pack(padx=10, pady=5)
        tk.Button(self.nav_frame, text="Найти маршрут", bg=self.theme.button_bg, fg=self.theme.button_fg,
                  relief="flat", command=self.search_route).pack(pady=2)
        self.route_text = tk.Text(self.nav_frame, bg=self.theme.bg_color, fg=self.theme.fg_color, height=15)
        self.route_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def search_route(self):
        coords = self.coords_entry.get().strip()
        if coords:
            self.route_text.delete(1.0, tk.END)
            self.route_text.insert(tk.END, f"Маршрут до {coords}\n1. Поверните направо\n2. Проедьте 2 км\n")
            self.coords_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Предупреждение","Введите координаты!")

    # ===== Карты =====
    def create_map_widgets(self):
        tk.Label(self.map_frame, text="Карты", bg=self.theme.bg_color, fg=self.theme.fg_color).pack(pady=20)

    # ===== Закрытие =====
    def on_close(self):
        self.autosave_tasks()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MultiTabApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
