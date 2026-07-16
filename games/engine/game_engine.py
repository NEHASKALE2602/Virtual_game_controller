from PySide6.QtWidgets import QWidget, QVBoxLayout


class GameEngine(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

    def load_game(self, game_widget):

        while self.layout.count():

            item = self.layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        self.layout.addWidget(game_widget)