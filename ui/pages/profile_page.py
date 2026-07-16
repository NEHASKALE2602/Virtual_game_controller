from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class ProfilePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        label = QLabel("👤 Profile")
        label.setStyleSheet("font-size:30px;font-weight:bold;")
        layout.addWidget(label)