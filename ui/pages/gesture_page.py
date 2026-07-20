from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QFrame,
    QSizePolicy
)

class GestureCard(QFrame):

    def __init__(self, emoji, title, line1="", line2=""):

        super().__init__()

        self.setObjectName("gestureCard")

        self.setMinimumSize(280, 220)

        self.setSizePolicy(

            QSizePolicy.Expanding,

            QSizePolicy.Expanding

        )
        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 20, 20, 20)

        layout.setSpacing(10)

        self.emoji = QLabel(emoji)
        self.emoji.setObjectName("gestureEmoji")
        self.emoji.setAlignment(Qt.AlignCenter)

        self.title = QLabel(title)
        self.title.setObjectName("gestureTitle")
        self.title.setAlignment(Qt.AlignCenter)

        self.line1 = QLabel(line1)
        self.line1.setObjectName("gestureInfo")
        self.line1.setAlignment(Qt.AlignCenter)

        self.line2 = QLabel(line2)
        self.line2.setObjectName("gestureInfo")
        self.line2.setAlignment(Qt.AlignCenter)

        layout.addStretch()

        layout.addWidget(self.emoji)

        layout.addWidget(self.title)

        layout.addSpacing(8)

        layout.addWidget(self.line1)

        layout.addWidget(self.line2)

        layout.addStretch()


class GesturePage(QWidget):

    def __init__(self):

        super().__init__()

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(40, 25, 40, 25)

        main_layout.setSpacing(20)

        title = QLabel("🎮 GAME CONTROLS")

        title.setObjectName("pageTitle")

        title.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title)

        self.grid = QGridLayout()
        self.grid.setColumnStretch(0, 1)

        self.grid.setColumnStretch(1, 1)

        self.grid.setColumnStretch(2, 1)

        self.grid.setRowStretch(0, 1)

        self.grid.setRowStretch(1, 1)

        self.grid.setHorizontalSpacing(25)

        self.grid.setVerticalSpacing(25)

        self.grid.setAlignment(Qt.AlignCenter)

        main_layout.addLayout(self.grid)
        # ======================================================
# FIRST ROW
# ======================================================

        self.open_palm = GestureCard(

            "✋",

            "OPEN PALM",

            "🍎 Fruit Ninja",

            "Slice Fruits"

        )

        self.pointing = GestureCard(

            "☝",

            "POINTING",

            "🚀 Space Shooter",

            "Move Spaceship"

        )

        self.fist = GestureCard(

            "✊",

            "FIST",

            "⏸ Pause Game",

            "Restart Game"

        )

        self.grid.addWidget(self.open_palm, 0, 0)

        self.grid.addWidget(self.pointing, 0, 1)

        self.grid.addWidget(self.fist, 0, 2)

        main_layout.addStretch()
# ======================================================
# SECOND ROW
# ======================================================

        self.thumb_up = GestureCard(

            "👍",

            "THUMB UP",

            "🎮 Future Feature",

            "Confirm Action"

        )

        self.direction = GestureCard(

            "⬅ ➡ ⬆ ⬇",

            "DIRECTION",

            "🚗 Racing Game",

            "Steering Control"

        )

        self.snake = GestureCard(

             "🐍",

            "SNAKE CONTROL",

            "☝ Point Finger",

            "Move Snake"

        )

        self.grid.addWidget(self.thumb_up, 1, 0)

        self.grid.addWidget(self.direction, 1, 1)

        self.grid.addWidget(self.snake, 1, 2)