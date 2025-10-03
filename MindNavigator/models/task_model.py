import json
import os
from datetime import datetime

class TaskModel:
    def __init__(self, autosave_file="tasks.json"):
        self.tasks = []
        self.completed_tasks = []
        self.autosave_file = autosave_file
        self.load_tasks()

    def add_task(self, task_data):
        self.tasks.append(task_data)
        self.autosave()

    def toggle_done(self, index):
        task = self.tasks[index]
        task["done"] = True
        self.completed_tasks.append(task)
        self.tasks.pop(index)
        self.autosave()

    def toggle_important(self, index):
        self.tasks[index]["important"] = not self.tasks[index].get("important", False)
        self.autosave()

    def autosave(self):
        try:
            with open(self.autosave_file, "w", encoding="utf-8") as f:
                json.dump({"tasks": self.tasks, "completed": self.completed_tasks}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("Ошибка автосохранения:", e)

    def load_tasks(self):
        if os.path.exists(self.autosave_file):
            try:
                with open(self.autosave_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])
                    self.completed_tasks = data.get("completed", [])
            except:
                self.tasks = []
                self.completed_tasks = []