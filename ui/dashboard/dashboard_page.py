from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QGridLayout,
    QVBoxLayout,
    QPushButton
)
class DashboardCard(QFrame):

    def __init__(self, title, value):
        super().__init__()

        self.setObjectName("dashboardCard")

        self.setMinimumHeight(140)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.title = QLabel(title)
        self.title.setObjectName("cardTitle")

        self.value = QLabel(value)
        self.value.setObjectName("cardValue")

        self.value.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.value)


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setSpacing(20)

    # ===========================================
    # Hero Banner
    # ===========================================

        self.banner = QLabel()

        self.banner.setObjectName("heroBanner")

        self.banner.setMinimumHeight(450)

        self.banner.setScaledContents(True)

        self.banner.setPixmap(QPixmap("assets/images/hero_bg.jpg"))

        self.layout.addWidget(self.banner)

    def update_card(self, title, value):
        pass