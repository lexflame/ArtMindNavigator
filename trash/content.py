from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class Content(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        label = QLabel("Рабочая область (контент)")
        layout.addWidget(label)
