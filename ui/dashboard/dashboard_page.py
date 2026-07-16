from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QGridLayout,
    QVBoxLayout,
    QSizePolicy
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

        self.layout = QGridLayout(self)

        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setHorizontalSpacing(20)
        self.layout.setVerticalSpacing(20)

        cards = [

            ("📷 Camera Status", "Disconnected"),

            ("🤖 AI Status", "Stopped"),

            ("✋ Current Gesture", "NO HAND"),

            ("🙌 Hands Detected", "0"),

            ("⚡ FPS", "0"),

            ("🎮 Current Game", "None"),

            ("🎯 Confidence", "0%"),

            ("🏆 High Score", "0")

        ]

        row = 0
        col = 0

        for title, value in cards:

            card = DashboardCard(title, value)

            if not hasattr(self, "cards"):
                self.cards = {}

            self.cards[title] = card

            self.layout.addWidget(card, row, col)

            col += 1

            if col == 2:
                col = 0
                row += 1
    def update_card(self, title, value):

        if title in self.cards:

            self.cards[title].value.setText(str(value))