from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class GesturePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        label = QLabel("✋ Gestures")
        label.setStyleSheet("font-size:30px;font-weight:bold;")
        layout.addWidget(label)