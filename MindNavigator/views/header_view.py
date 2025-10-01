import tkinter as tk
from config import DarkTheme

class HeaderView:
    def __init__(self, root):
        self.root = root
        self.theme = DarkTheme
        self.create_header()

    def create_header(self):
        self.title_bar = tk.Frame(self.root, bg=self.theme.TITLE_BAR_BG, height=40)
        self.title_bar.pack(fill=tk.X)
        self.title_label = tk.Label(self.title_bar, text="MindNavigator",
                                    bg=self.theme.TITLE_BAR_BG, fg=self.theme.FG_COLOR,
                                    font=("Helvetica", 12, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=5)
        self.btn_close = tk.Button(self.title_bar, text="✕", command=self.root.destroy,
                                   bg="#FF5555", fg="white", relief="flat", width=4)
        self.btn_close.pack(side=tk.RIGHT, padx=2)
