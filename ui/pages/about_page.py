from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class AboutPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        label = QLabel("ℹ About")
        label.setStyleSheet("font-size:30px;font-weight:bold;")
        layout.addWidget(label)