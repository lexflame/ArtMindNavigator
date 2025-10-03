import sys
from PyQt6.QtWidgets import QApplication

import tkinter as tk
from config import DarkTheme

from views.window.main_window import MainWindow

from models.task_model import TaskModel
from models.note_model import NoteModel

from views.task.task_view import TaskView
from views.note.note_view import NoteView
from views.map.map_view import MapView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
