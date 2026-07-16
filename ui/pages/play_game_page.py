from PySide6.QtWidgets import QWidget, QVBoxLayout

from ui.game_window.game_window import GameWindow


class PlayGamePage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.game_window = GameWindow()

        layout.addWidget(self.game_window)