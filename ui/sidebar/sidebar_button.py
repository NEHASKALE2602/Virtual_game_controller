from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


class SidebarButton(QPushButton):
    """
    Reusable Sidebar Button
    """

    def __init__(self, icon: str, text: str):
        super().__init__()

        self.setText(f"{icon}   {text}")

        self.setCursor(Qt.PointingHandCursor)

        self.setFixedHeight(55)

        self.setMinimumWidth(220)

        self.setObjectName("sidebarButton")