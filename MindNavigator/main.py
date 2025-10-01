import tkinter as tk
from config import DarkTheme
from models.task_model import TaskModel
from models.note_model import NoteModel
from views.header_view import HeaderView
from views.task_view import TaskView
from views.note_view import NoteView
from views.map_view import MapView
from views.nav_view import NavView

def main():
    root = tk.Tk()
    root.overrideredirect(True)
    root.state("zoomed")
    root.config(bg=DarkTheme.BG_COLOR)

    task_model = TaskModel()
    note_model = NoteModel()

    header = HeaderView(root)
    task_view = TaskView(root, task_model)
    note_view = NoteView(root, note_model)
    map_view = MapView(root)
    nav_view = NavView(root)

    root.mainloop()

if __name__ == "__main__":
    main()
