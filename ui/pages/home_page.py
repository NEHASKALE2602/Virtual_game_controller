from PySide6.QtWidgets import QWidget, QVBoxLayout

from ui.dashboard.dashboard_page import DashboardPage


class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        dashboard = DashboardPage()

        layout.addWidget(dashboard)