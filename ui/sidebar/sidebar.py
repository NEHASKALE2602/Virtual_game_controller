from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy
)


class Sidebar(QWidget):

    page_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("sidebar")
        self.setFixedWidth(260)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        
        # ==========================================
        # Navigation Buttons
        # ==========================================

        self.buttons = {}
            # Home
        self.home_btn = QPushButton("  🏠   Home")
        self.home_btn.setObjectName("sidebarButton")
        self.home_btn.setMinimumHeight(48)
        self.home_btn.clicked.connect(
            lambda: self.change_page("home")
        )
        self.main_layout.addWidget(self.home_btn)
        self.buttons["home"] = self.home_btn

        # Games
        self.games_btn = QPushButton("  🎮   Games")
        self.games_btn.setObjectName("sidebarButton")
        self.games_btn.setMinimumHeight(48)
        self.games_btn.clicked.connect(
            lambda: self.change_page("games")
        )
        self.main_layout.addWidget(self.games_btn)
        self.buttons["games"] = self.games_btn

        # Camera
        self.camera_btn = QPushButton("  📷   Camera")
        self.camera_btn.setObjectName("sidebarButton")
        self.camera_btn.setMinimumHeight(48)
        self.camera_btn.clicked.connect(
            lambda: self.change_page("camera")
        )
        self.main_layout.addWidget(self.camera_btn)
        self.buttons["camera"] = self.camera_btn

        # Gesture
        self.gesture_btn = QPushButton("  ✋   Gesture")
        self.gesture_btn.setObjectName("sidebarButton")
        self.gesture_btn.setMinimumHeight(48)
        self.gesture_btn.clicked.connect(
            lambda: self.change_page("gesture")
        )
        self.main_layout.addWidget(self.gesture_btn)
        self.buttons["gesture"] = self.gesture_btn

        # Analytics
        self.analytics_btn = QPushButton("  📊   Analytics")
        self.analytics_btn.setObjectName("sidebarButton")
        self.analytics_btn.setMinimumHeight(48)
        self.analytics_btn.clicked.connect(
            lambda: self.change_page("analytics")
        )
        self.main_layout.addWidget(self.analytics_btn)
        self.buttons["analytics"] = self.analytics_btn

        # Profile
        self.profile_btn = QPushButton("  👤   Profile")
        self.profile_btn.setObjectName("sidebarButton")
        self.profile_btn.setMinimumHeight(48)
        self.profile_btn.clicked.connect(
            lambda: self.change_page("profile")
        )
        self.main_layout.addWidget(self.profile_btn)
        self.buttons["profile"] = self.profile_btn

        # Settings
        self.settings_btn = QPushButton("  ⚙   Settings")
        self.settings_btn.setObjectName("sidebarButton")
        self.settings_btn.setMinimumHeight(48)
        self.settings_btn.clicked.connect(
            lambda: self.change_page("settings")
        )
        self.main_layout.addWidget(self.settings_btn)
        self.buttons["settings"] = self.settings_btn

        # About
        self.about_btn = QPushButton("  ℹ   About")
        self.about_btn.setObjectName("sidebarButton")
        self.about_btn.setMinimumHeight(48)
        self.about_btn.clicked.connect(
            lambda: self.change_page("about")
        )
        self.main_layout.addWidget(self.about_btn)

        self.buttons["about"] = self.about_btn
                # ==========================================
        # Push Bottom
        # ==========================================

        self.main_layout.addStretch()

        # ==========================================
        # Online Status
        # ==========================================

        self.status_label = QLabel("🟢  AI Engine Online")
        self.status_label.setObjectName("versionLabel")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.status_label)

        # ==========================================
        # Version
        # ==========================================

        self.version_label = QLabel("Version 2.0")
        self.version_label.setObjectName("versionLabel")
        self.version_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.version_label)

        # ==========================================
        # Select Default Page
        # ==========================================

        self.change_page("home")

    # =====================================================
    # Change Active Page
    # =====================================================

    def change_page(self, page):

        # Reset all buttons

        for btn in self.buttons.values():

            btn.setStyleSheet("")

        # Highlight selected button

        if page in self.buttons:

            self.buttons[page].setStyleSheet("""

                QPushButton{

                    background:#2563EB;

                    color:white;

                    border:none;

                    border-radius:14px;

                    font-weight:bold;

                    text-align:left;

                    padding-left:18px;

                }

            """)

        self.page_changed.emit(page)
        # =====================================================
    # Get Current Button
    # =====================================================

    def get_button(self, page):

        return self.buttons.get(page)

    # =====================================================
    # Enable / Disable Buttons
    # =====================================================

    def set_buttons_enabled(self, enabled=True):

        for button in self.buttons.values():

            button.setEnabled(enabled)

    # =====================================================
    # Highlight Button Externally
    # =====================================================

    def set_active_page(self, page):

        self.change_page(page)

    # =====================================================
    # Update Status Text
    # =====================================================

    def set_status(self, text):

        self.status_label.setText(text)

    # =====================================================
    # Update Version
    # =====================================================

    def set_version(self, version):

        self.version_label.setText(version)