from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame
)


class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        # ==================================================
        # Main Layout
        # ==================================================

        self.mainLayout = QVBoxLayout(self)

        self.mainLayout.setContentsMargins(25, 25, 25, 25)

        self.mainLayout.setSpacing(20)

        # ==================================================
        # Hero Card
        # ==================================================

        self.heroCard = QFrame()

        self.heroCard.setObjectName("heroCard")

        self.heroLayout = QVBoxLayout(self.heroCard)

        self.heroLayout.setContentsMargins(30, 30, 30, 30)

        # Title

        self.title = QLabel("🎮 Virtual Game Controller")

        self.title.setObjectName("heroTitle")

        self.heroLayout.addWidget(self.title)

        # Subtitle

        self.subtitle = QLabel(
            "Control Games Using AI Hand Gestures"
        )

        self.subtitle.setObjectName("heroSubtitle")

        self.heroLayout.addWidget(self.subtitle)

        # ==================================================
        # Buttons
        # ==================================================

        self.buttonLayout = QHBoxLayout()

        self.playButton = QPushButton("▶ Play Games")
        self.playButton.setObjectName("modernButton")

        self.cameraButton = QPushButton("📷 Open Camera")
        self.cameraButton.setObjectName("modernButton")

        self.analyticsButton = QPushButton("📊 Analytics")
        self.analyticsButton.setObjectName("modernButton")

        self.buttonLayout.addWidget(self.playButton)
        self.buttonLayout.addWidget(self.cameraButton)
        self.buttonLayout.addWidget(self.analyticsButton)

        self.buttonLayout.addStretch()

        self.heroLayout.addLayout(self.buttonLayout)

        self.mainLayout.addWidget(self.heroCard)
# ==================================================
# Premium Gaming Banner
# ==================================================

        self.banner = QFrame()
        self.banner.setObjectName("heroBanner")
        self.banner.setMinimumHeight(420)

        bannerLayout = QVBoxLayout(self.banner)

        bannerLayout.setContentsMargins(50, 50, 50, 50)

        bannerLayout.addStretch()

# =====================================
# Welcome
# =====================================

        welcome = QLabel("👋 Welcome Back")
        welcome.setObjectName("heroWelcome")
        bannerLayout.addWidget(welcome)

# =====================================
# Main Title
# =====================================

        title = QLabel("Virtual Game Controller")
        title.setObjectName("heroMainTitle")
        bannerLayout.addWidget(title)

# =====================================
# Subtitle
# =====================================

        subtitle = QLabel(
            "Play games naturally using AI-powered hand gestures."
        )

        subtitle.setObjectName("heroSubTitle")
        bannerLayout.addWidget(subtitle)

        bannerLayout.addSpacing(20)

# =====================================
# Play Button
# =====================================

        playButton = QPushButton("▶ PLAY NOW")
        playButton.setObjectName("heroButton")
        playButton.setFixedSize(220, 55)

        bannerLayout.addWidget(playButton)

        bannerLayout.addStretch()

        self.mainLayout.addWidget(self.banner)