import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkinter import filedialog
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

        file_frame = tk.Frame(self.task_frame, bg=self.theme.bg_color)
        file_frame.pack(pady=5)

        save_button = tk.Button(
            file_frame, text="Сохранить", command=self.save_tasks,
            bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", width=12
        )
        save_button.pack(side=tk.LEFT, padx=5)

        load_button = tk.Button(
            file_frame, text="Загрузить", command=self.load_tasks,
            bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", width=12
        )
        load_button.pack(side=tk.LEFT, padx=5)

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
        # Поле ввода задачи
        tk.Label(self.task_frame, text="Название задачи:", bg=self.theme.bg_color, fg=self.theme.fg_color).pack(
            pady=(5, 0), padx=10, anchor="w")
        self.task_entry = tk.Entry(
            self.task_frame,
            width=50,
            bg=self.theme.entry_bg,
            fg=self.theme.entry_fg,
            borderwidth=0
        )
        self.task_entry.pack(pady=2, padx=10)

        # Поле ввода срока
        tk.Label(self.task_frame, text="Срок выполнения (ДД.ММ.ГГГГ):", bg=self.theme.bg_color,
                 fg=self.theme.fg_color).pack(pady=(5, 0), padx=10, anchor="w")
        self.due_entry = tk.Entry(
            self.task_frame,
            width=20,
            bg=self.theme.entry_bg,
            fg=self.theme.entry_fg,
            borderwidth=0
        )
        self.due_entry.pack(pady=2, padx=10)

        # Поле описания
        tk.Label(self.task_frame, text="Описание:", bg=self.theme.bg_color, fg=self.theme.fg_color).pack(pady=(5, 0),
                                                                                                         padx=10,
                                                                                                         anchor="w")
        self.desc_text = tk.Text(
            self.task_frame,
            width=50,
            height=4,
            bg=self.theme.entry_bg,
            fg=self.theme.entry_fg,
            borderwidth=0,
            highlightthickness=0
        )
        self.desc_text.pack(pady=2, padx=10)

        # Приоритет
        tk.Label(self.task_frame, text="Приоритет:", bg=self.theme.bg_color, fg=self.theme.fg_color).pack(pady=(5, 0),
                                                                                                          padx=10,
                                                                                                          anchor="w")
        self.priority_var = tk.StringVar(value="Средний")
        priorities = ["Низкий", "Средний", "Высокий"]
        self.priority_menu = ttk.Combobox(self.task_frame, textvariable=self.priority_var, values=priorities,
                                          state="readonly", width=15)
        self.priority_menu.pack(pady=2, padx=10)

        # Кнопка добавления
        add_button = tk.Button(
            self.task_frame, text="Добавить", command=self.add_task,
            bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat"
        )
        add_button.pack(pady=5)

        # Список задач
        self.task_list = tk.Listbox(
            self.task_frame,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            selectbackground=self.theme.accent_color,
            selectforeground=self.theme.fg_color,
            borderwidth=0,
            highlightthickness=0,
            width=80,
            height=10
        )
        self.task_list.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Привязка выбора задачи для редактирования
        self.task_list.bind("<<ListboxSelect>>", self.on_task_select)

        # Кнопки редактирования и удаления
        btn_frame = tk.Frame(self.task_frame, bg=self.theme.bg_color)
        btn_frame.pack(pady=5)

        update_button = tk.Button(
            btn_frame, text="Обновить", command=self.update_task,
            bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", width=12
        )
        update_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(
            btn_frame, text="Удалить", command=self.delete_task,
            bg=self.theme.button_bg, fg=self.theme.button_fg, relief="flat", width=12
        )
        delete_button.pack(side=tk.LEFT, padx=5)

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
        task = self.task_entry.get().strip()
        due = self.due_entry.get().strip()
        desc = self.desc_text.get("1.0", tk.END).strip()
        priority = self.priority_var.get()

        if not task:
            messagebox.showwarning("Предупреждение", "Введите название задачи!")
            return

        # Формат отображения в списке
        display_text = f"[{priority}] {task} (Срок: {due})"
        if desc:
            display_text += f" - {desc}"

        self.tasks.append({
            "task": task,
            "due": due,
            "desc": desc,
            "priority": priority
        })

        self.task_list.insert(tk.END, display_text)

        # Очистка полей
        self.task_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.priority_var.set("Средний")

    def on_task_select(self, event):
        """Заполняем поля для редактирования выбранной задачи"""
        try:
            index = self.task_list.curselection()[0]
            task = self.tasks[index]

            # Заполняем поля
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, task["task"])

            self.due_entry.delete(0, tk.END)
            self.due_entry.insert(0, task["due"])

            self.desc_text.delete("1.0", tk.END)
            self.desc_text.insert(tk.END, task["desc"])

            self.priority_var.set(task["priority"])
        except IndexError:
            pass  # ничего не делаем, если ничего не выбрано

    def update_task(self):
        """Обновление выбранной задачи"""
        try:
            index = self.task_list.curselection()[0]
            task = self.task_entry.get().strip()
            due = self.due_entry.get().strip()
            desc = self.desc_text.get("1.0", tk.END).strip()
            priority = self.priority_var.get()

            if not task:
                messagebox.showwarning("Предупреждение", "Введите название задачи!")
                return

            # Обновляем данные
            self.tasks[index] = {
                "task": task,
                "due": due,
                "desc": desc,
                "priority": priority
            }

            # Обновляем отображение в Listbox
            display_text = f"[{priority}] {task} (Срок: {due})"
            if desc:
                display_text += f" - {desc}"

            self.task_list.delete(index)
            self.task_list.insert(index, display_text)
        except IndexError:
            messagebox.showwarning("Предупреждение", "Выберите задачу для редактирования!")

    def delete_task(self):
        """Удаление выбранной задачи"""
        try:
            index = self.task_list.curselection()[0]
            self.task_list.delete(index)
            self.tasks.pop(index)
        except IndexError:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления!")

    # ==== Методы для сохранения и загрузки ====

    def save_tasks(self):
        """Сохраняем задачи в выбранный файл"""
        file_path = filedialog.asksaveasfilename(
            title="Сохранить задачи",
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.tasks, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Сохранение", f"Задачи сохранены в {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def load_tasks(self):
        """Загружаем задачи из выбранного файла"""
        file_path = filedialog.askopenfilename(
            title="Открыть задачи",
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    loaded_tasks = json.load(f)
                self.tasks = loaded_tasks
                # Обновляем Listbox
                self.task_list.delete(0, tk.END)
                for t in self.tasks:
                    display_text = f"[{t['priority']}] {t['task']} (Срок: {t['due']})"
                    if t['desc']:
                        display_text += f" - {t['desc']}"
                    self.task_list.insert(tk.END, display_text)
                messagebox.showinfo("Загрузка", f"Задачи загружены из {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")

def main():
    root = tk.Tk()
    app = MultiTabApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
