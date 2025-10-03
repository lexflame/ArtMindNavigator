import tkinter as tk
from config import DarkTheme

class MapView:
    def __init__(self, root):
        self.frame = tk.Frame(root, bg=DarkTheme.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.frame, text="Карты", bg=DarkTheme.BG_COLOR, fg=DarkTheme.FG_COLOR).pack(pady=20)