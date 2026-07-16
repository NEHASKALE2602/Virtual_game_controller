from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class SpaceShooterGame(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("🚀 Space Shooter")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:30px;
            color:white;
            font-weight:bold;
        """)

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()