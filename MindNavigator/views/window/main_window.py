from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation
from views.window.title_bar import TitleBar
from views.window.resources import APP_BACKGROUND, FONT_COLOR, BUTTON_BG, BUTTON_HOVER

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(f"background-color: {APP_BACKGROUND}; color: {FONT_COLOR}; font-family: Arial;")
        self.setMinimumSize(800, 500)

        # Боковая панель (гамбургер-меню)
        self.side_menu = QFrame(self)
        self.side_menu.setGeometry(-200, 40, 200, self.height())  # скрыта за пределами окна
        self.side_menu.setStyleSheet(f"background-color: {BUTTON_BG}; color: {FONT_COLOR};")
        self.side_menu.setFixedWidth(200)

        # Контент боковой панели
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

        # Анимация боковой панели
        self.menu_animation = QPropertyAnimation(self.side_menu, b"geometry")
        self.menu_animation.setDuration(250)

        # Заголовок с гамбургером
        self.title_bar = TitleBar(self, toggle_menu_callback=self.toggle_menu)

        # Контент окна
        self.content = QLabel("Привет! Это окно с современным гамбургер-меню.")
        self.content.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Главный лэйаут
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.content)
        self.setLayout(main_layout)

        # Разворачиваем окно на весь экран
        screen_geometry = self.screen().availableGeometry()
        self.setGeometry(screen_geometry)

        self.menu_visible = False

    def toggle_menu(self):
        if self.menu_visible:
            start_geom = self.side_menu.geometry()
            end_geom = start_geom.translated(-self.side_menu.width(), 0)
        else:
            start_geom = self.side_menu.geometry()
            end_geom = start_geom.translated(self.side_menu.width(), 0)

        self.menu_animation.stop()
        self.menu_animation.setStartValue(start_geom)
        self.menu_animation.setEndValue(end_geom)
        self.menu_animation.start()

        self.menu_visible = not self.menu_visible
