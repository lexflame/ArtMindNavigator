from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QSize
import qtawesome as qta

class SideBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedWidth(200)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Кнопки с иконками
        self.home_btn = self._make_button("fa5s.home", "Главная")
        self.tasks_btn = self._make_button("fa5s.folder", "Задачи")
        self.notes_btn = self._make_button("fa5s.sticky-note", "Заметки")
        self.stats_btn = self._make_button("mdi.chart-bar", "Статистика")
        self.settings_btn = self._make_button("fa5s.cog", "Настройки")

        # Добавляем кнопки в панель
        for btn in [self.home_btn, self.tasks_btn, self.notes_btn, self.stats_btn, self.settings_btn]:
            layout.addWidget(btn)

        layout.addStretch()

    def _make_button(self, icon_name, text):
        """Создание кнопки с иконкой и текстом"""
        icon = qta.icon(icon_name, color="white")
        btn = QPushButton(icon, text)
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: white;
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)
        btn.setIconSize(QSize(16, 16))
        return btn
