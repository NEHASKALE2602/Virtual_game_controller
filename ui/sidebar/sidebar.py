from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QSizePolicy
)

from ui.sidebar.sidebar_button import SidebarButton


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("sidebar")

        self.setFixedWidth(240)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(15, 20, 15, 20)
        self.main_layout.setSpacing(12)

        self.setLayout(self.main_layout)

        # ---------------- Logo ----------------
        self.logo = QLabel("🎮 VIRTUAL GAME\nCONTROLLER")
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setObjectName("logoLabel")

        self.main_layout.addWidget(self.logo)

        # ---------------- Menu ----------------
        self.home_btn = SidebarButton("🏠", "Home")
        self.games_btn = SidebarButton("🎮", "Games")
        self.camera_btn = SidebarButton("📷", "Camera")
        self.gesture_btn = SidebarButton("✋", "Gestures")
        self.analytics_btn = SidebarButton("📊", "Analytics")
        self.profile_btn = SidebarButton("👤", "Profile")
        self.settings_btn = SidebarButton("⚙", "Settings")
        self.about_btn = SidebarButton("ℹ", "About")

        self.main_layout.addWidget(self.home_btn)
        self.main_layout.addWidget(self.games_btn)
        self.main_layout.addWidget(self.camera_btn)
        self.main_layout.addWidget(self.gesture_btn)
        self.main_layout.addWidget(self.analytics_btn)
        self.main_layout.addWidget(self.profile_btn)
        self.main_layout.addWidget(self.settings_btn)
        self.main_layout.addWidget(self.about_btn)

        # Push version label to bottom
        self.main_layout.addStretch()

        # ---------------- Footer ----------------
        self.version = QLabel("Version 1.0")
        self.version.setAlignment(Qt.AlignCenter)
        self.version.setObjectName("versionLabel")

        self.main_layout.addWidget(self.version)