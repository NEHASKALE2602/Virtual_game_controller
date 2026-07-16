from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel


class StatusBar(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("statusBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5)

        self.fps = QLabel("FPS : 0")
        self.camera = QLabel("📷 Camera : OFF")
        self.ai = QLabel("🤖 AI : OFF")
        self.gesture = QLabel("✋ Gesture : NONE")
        self.version = QLabel("Version : 1.0")

        layout.addWidget(self.fps)
        layout.addStretch()
        layout.addWidget(self.camera)
        layout.addSpacing(20)
        layout.addWidget(self.ai)
        layout.addSpacing(20)
        layout.addWidget(self.gesture)
        layout.addSpacing(20)
        layout.addWidget(self.version)