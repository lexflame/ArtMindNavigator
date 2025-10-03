import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk
from datetime import datetime
from utils.drag_drop import make_draggable
from config import DarkTheme

class TaskView:
    def __init__(self, root, task_model):
        self.root = root
        self.model = task_model
        self.theme = DarkTheme
        self.frame = tk.Frame(root, bg=self.theme.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.refresh_task_list()

        layout_menu = QVBoxLayout()
        layout_menu.setContentsMargins(0, 0, 0, 0)
        for name in ["Главная", "Настройки", "Синхронизация", "Выход"]:
            btn = QPushButton(name)
            btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {BUTTON_BG};
                            color: {FONT_COLOR};
                            border: none;
                            padding: 10px;
                            text-align: left;
                        }}
                        QPushButton:hover {{
                            background-color: {BUTTON_HOVER};
                        }}
                    """)
            if name == "Выход":
                btn.clicked.connect(self.close)
            layout_menu.addWidget(btn)
        layout_menu.addStretch()
        self.side_menu.setLayout(layout_menu)

    def create_widgets(self):
        self.input_frame = tk.Frame(self.frame, bg=self.theme.BG_COLOR)
        self.input_frame.pack(fill=tk.X, pady=5, padx=10)
        self.task_entry = tk.Entry(self.input_frame, bg=self.theme.ENTRY_BG, fg=self.theme.ENTRY_FG)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.desc_entry = tk.Entry(self.input_frame, bg=self.theme.ENTRY_BG, fg=self.theme.ENTRY_FG)
        self.desc_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.date_entry = DateEntry(self.input_frame, width=12, background='darkblue', foreground='white', date_pattern='dd.mm.yyyy')
        self.date_entry.pack(side=tk.LEFT, padx=2)
        self.hour_var = tk.StringVar(value="12")
        self.minute_var = tk.StringVar(value="00")
        self.hour_cb = ttk.Combobox(self.input_frame, width=3, textvariable=self.hour_var, values=[f"{i:02d}" for i in range(24)], state="readonly")
        self.hour_cb.pack(side=tk.LEFT)
        self.minute_cb = ttk.Combobox(self.input_frame, width=3, textvariable=self.minute_var, values=[f"{i:02d}" for i in range(60)], state="readonly")
        self.minute_cb.pack(side=tk.LEFT)
        self.priority_var = tk.StringVar(value="Средний")
        self.priority_menu = ttk.Combobox(self.input_frame, textvariable=self.priority_var, values=["Низкий","Средний","Высокий"], state="readonly", width=10)
        self.priority_menu.pack(side=tk.LEFT, padx=2)
        add_btn = tk.Button(self.input_frame, text="Добавить", command=self.add_task, bg=self.theme.BUTTON_BG, fg=self.theme.BUTTON_FG, relief="flat")
        add_btn.pack(side=tk.LEFT, padx=2)
        self.task_list_frame = tk.Frame(self.frame, bg=self.theme.BG_COLOR)
        self.task_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def add_task(self):
        task = self.task_entry.get().strip()
        desc = self.desc_entry.get().strip()
        date = self.date_entry.get_date().strftime("%d.%m.%Y")
        time = f"{self.hour_var.get()}:{self.minute_var.get()}"
        due = f"{date} {time}"
        priority = self.priority_var.get()
        if not task:
            return
        self.model.add_task({"task": task, "desc": desc, "due": due, "priority": priority, "done": False, "important": False})
        self.clear_task_form()
        self.refresh_task_list()

    def refresh_task_list(self):
        for w in self.task_list_frame.winfo_children():
            w.destroy()
        for i, t in enumerate(self.model.tasks):
            frame = tk.Frame(self.task_list_frame, bg=self.theme.ENTRY_BG, bd=1, relief="solid")
            frame.pack(fill=tk.X, padx=5, pady=3)
            var = tk.BooleanVar(value=t["done"])
            chk = tk.Checkbutton(frame, variable=var, bg=self.theme.ENTRY_BG,
                                 command=lambda i=i,v=var: self.model.toggle_done(i))
            chk.pack(side=tk.LEFT, padx=5)
            star_btn = tk.Button(frame, text="★" if t.get("important", False) else "☆",
                                 bg=self.theme.ENTRY_BG, fg="#FFD700", relief="flat",
                                 command=lambda i=i: self.model.toggle_important(i))
            star_btn.pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"{t['task']} ({t['due']})", bg=self.theme.ENTRY_BG, fg=self.theme.FG_COLOR).pack(side=tk.LEFT)
            if t["desc"]:
                tk.Label(frame, text=t["desc"], bg=self.theme.ENTRY_BG, fg=self.theme.FG_COLOR).pack(side=tk.LEFT)
            make_draggable(frame, self.refresh_task_list)

    def clear_task_form(self):
        self.task_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)