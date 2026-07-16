from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout
)

from ui.game_cards.game_card import GameCard


class GamesPage(QWidget):

    game_selected = Signal(str)

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        title = QLabel("🎮 Game Library")
        title.setObjectName("pageTitle")

        grid = QGridLayout()
        grid.setSpacing(20)

        games = [

            ("🏎", "Racing", "Control the racing car using hand gestures."),

            ("🐦", "Flappy Bird", "Fly the bird using your hand."),

            ("🍉", "Fruit Ninja", "Slice fruits using hand swipes."),

            ("🚀", "Space Shooter", "Move and shoot using gestures."),

            ("🐍", "Snake", "Control the snake with hand movement.")

        ]

        row = 0
        col = 0

        for icon, name, desc in games:

            card = GameCard(icon, name, desc)

            card.play_clicked.connect(self.game_selected.emit)

            grid.addWidget(card, row, col)

            col += 1

            if col == 3:
                col = 0
                row += 1

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()