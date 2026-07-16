from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy
)

from datetime import datetime


class TopBar(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("topBar")
        self.setFixedHeight(80)

        self.main_layout = QHBoxLayout(self)

        self.main_layout.setContentsMargins(20, 10, 20, 10)

        self.main_layout.setSpacing(15)

        # =====================================
        # Title
        # =====================================

        self.titleLabel = QLabel("Virtual Game Controller")

        self.titleLabel.setObjectName("titleLabel")

        self.main_layout.addWidget(self.titleLabel)

        self.main_layout.addStretch()

        # =====================================
        # Search Box
        # =====================================

        self.searchBox = QLineEdit()

        self.searchBox.setObjectName("searchBox")

        self.searchBox.setPlaceholderText("Search games...")

        self.main_layout.addWidget(self.searchBox)
                # =====================================
        # Notification Button
        # =====================================

        self.notificationButton = QPushButton("🔔")

        self.notificationButton.setObjectName("topButton")

        self.notificationButton.setToolTip("Notifications")

        self.main_layout.addWidget(self.notificationButton)

        # =====================================
        # Theme Button
        # =====================================

        self.themeButton = QPushButton("🌙")

        self.themeButton.setObjectName("topButton")

        self.themeButton.setToolTip("Dark Mode")

        self.main_layout.addWidget(self.themeButton)

        # =====================================
        # Live Clock
        # =====================================

        self.clockLabel = QLabel()

        self.clockLabel.setObjectName("titleLabel")

        self.main_layout.addWidget(self.clockLabel)

        self.timer = QTimer()

        self.timer.timeout.connect(self.update_time)

        self.timer.start(1000)

        self.update_time()
                # =====================================
        # Welcome Label
        # =====================================

        self.welcomeLabel = QLabel("👋 Welcome, Neha")

        self.welcomeLabel.setObjectName("titleLabel")

        self.main_layout.addWidget(self.welcomeLabel)

        # =====================================
        # Profile Button
        # =====================================

        self.profileButton = QPushButton("👤")

        self.profileButton.setObjectName("topButton")

        self.profileButton.setToolTip("Profile")

        self.main_layout.addWidget(self.profileButton)

        # =====================================
        # Settings Button
        # =====================================

        self.settingsButton = QPushButton("⚙")

        self.settingsButton.setObjectName("topButton")

        self.settingsButton.setToolTip("Settings")

        self.main_layout.addWidget(self.settingsButton)

    # ======================================================
    # Update Live Time
    # ======================================================

    def update_time(self):

        current = datetime.now().strftime("%I:%M:%S %p")

        self.clockLabel.setText(current)