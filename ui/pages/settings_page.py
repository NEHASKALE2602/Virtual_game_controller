from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        label = QLabel("⚙ Settings")
        label.setStyleSheet("font-size:30px;font-weight:bold;")
        layout.addWidget(label)