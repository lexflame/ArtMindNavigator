import tkinter as tk
from config import DarkTheme

class NoteView:
    def __init__(self, root, note_model):
        self.frame = tk.Frame(root, bg=DarkTheme.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.text = tk.Text(self.frame, bg=DarkTheme.BG_COLOR, fg=DarkTheme.FG_COLOR)
        self.text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)