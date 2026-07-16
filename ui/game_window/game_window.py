from PySide6.QtWidgets import QWidget, QVBoxLayout


class GameWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

    def show_game(self, game):

        while self.layout.count():

            item = self.layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        self.layout.addWidget(game)