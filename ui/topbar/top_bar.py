from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit
)


class TopBar(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("topBar")
        self.setFixedHeight(70)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(15)

        # Project Title
        title = QLabel("🎮 Virtual Game Controller")
        title.setObjectName("titleLabel")

        # Search Box
        search = QLineEdit()
        search.setPlaceholderText("Search...")
        search.setObjectName("searchBox")

        # Buttons
        notification = QPushButton("🔔")
        notification.setObjectName("topButton")

        theme = QPushButton("🌙")
        theme.setObjectName("topButton")

        fullscreen = QPushButton("🖥")
        fullscreen.setObjectName("topButton")

        profile = QPushButton("👤")
        profile.setObjectName("topButton")

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(search)
        layout.addWidget(notification)
        layout.addWidget(theme)
        layout.addWidget(fullscreen)
        layout.addWidget(profile)