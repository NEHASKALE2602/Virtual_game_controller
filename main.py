import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    style_file = Path("ui/styles/style.qss")

    if style_file.exists():
        with open(style_file, "r") as file:
            app.setStyleSheet(file.read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()