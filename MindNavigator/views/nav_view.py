import tkinter as tk
from config import DarkTheme

class NavView:
    def __init__(self, root):
        self.frame = tk.Frame(root, bg=DarkTheme.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.frame, text="Навигатор", bg=DarkTheme.BG_COLOR, fg=DarkTheme.FG_COLOR).pack(pady=10)
        self.coords_entry = tk.Entry(self.frame, bg=DarkTheme.ENTRY_BG, fg=DarkTheme.ENTRY_FG)
        self.coords_entry.pack(padx=10, pady=5)
        self.route_text = tk.Text(self.frame, bg=DarkTheme.BG_COLOR, fg=DarkTheme.FG_COLOR, height=15)
        self.route_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
