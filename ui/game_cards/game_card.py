from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QPushButton
)


class GameCard(QFrame):

    play_clicked = Signal(str)

    def __init__(self, icon, title, description):
        super().__init__()

        self.game_name = title

        self.setObjectName("gameCard")
        self.setFixedSize(260, 260)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setObjectName("gameIcon")

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("gameTitle")

        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setObjectName("gameDescription")

        self.play_button = QPushButton("▶ Play")
        self.play_button.setObjectName("playButton")

        self.play_button.clicked.connect(self.play_game)

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        layout.addWidget(self.play_button)

    def play_game(self):
        self.play_clicked.emit(self.game_name)