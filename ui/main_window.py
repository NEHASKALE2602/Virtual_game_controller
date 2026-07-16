from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt
from ui.topbar.top_bar import TopBar
from ui.dashboard.dashboard_page import DashboardPage
from PySide6.QtWidgets import QStackedWidget
from ui.sidebar.sidebar import Sidebar
from ui.pages.home_page import HomePage
from ui.pages.games_page import GamesPage
from ui.pages.camera_page import CameraPage
from ui.pages.gesture_page import GesturePage
from ui.pages.analytics_page import AnalyticsPage
from ui.pages.profile_page import ProfilePage
from ui.pages.settings_page import SettingsPage
from ui.pages.about_page import AboutPage
from ui.statusbar.status_bar import StatusBar
from ui.pages.play_game_page import PlayGamePage
from games.snake.snake_game import SnakeGame
from games.racing.racing_game import RacingGame
from games.flappy.flappy_game import FlappyGame
from games.fruit_ninja.fruit_ninja_game import FruitNinjaGame
from games.space_shooter.space_shooter_game import SpaceShooterGame


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Virtual Game Controller")
        self.resize(1400, 850)
        self.setMinimumSize(1200, 700)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Vertical Layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------------- Top Bar ----------------
        self.top_bar = TopBar()

        # ---------------- Middle Layout ----------------
        middle_layout = QHBoxLayout()
        middle_layout.setContentsMargins(0, 0, 0, 0)
        middle_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()

        # Main Content
        self.stack = QStackedWidget()

        self.home_page = DashboardPage()
        self.games_page = GamesPage()
        self.camera_page = CameraPage()
        self.camera_page.dashboard = self.home_page
        self.home_page.update_card("🎮 Current Game", "None")
        self.gesture_page = GesturePage()
        self.analytics_page = AnalyticsPage()
        self.profile_page = ProfilePage()
        self.settings_page = SettingsPage()
        self.about_page = AboutPage()
        self.play_game_page = PlayGamePage()

        self.stack.addWidget(self.home_page)        # Index 0
        self.stack.addWidget(self.games_page)       # Index 1
        self.stack.addWidget(self.camera_page)      # Index 2
        self.stack.addWidget(self.gesture_page)     # Index 3
        self.stack.addWidget(self.analytics_page)   # Index 4
        self.stack.addWidget(self.profile_page)     # Index 5
        self.stack.addWidget(self.settings_page)    # Index 6
        self.stack.addWidget(self.about_page)       # Index 7
        self.stack.addWidget(self.play_game_page)      # Index 8
        self.content = self.stack

        middle_layout.addWidget(self.sidebar)
        middle_layout.addWidget(self.content)

        self.sidebar.home_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.sidebar.games_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.sidebar.camera_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.sidebar.gesture_btn.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        self.sidebar.analytics_btn.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        self.sidebar.profile_btn.clicked.connect(lambda: self.stack.setCurrentIndex(5))
        self.sidebar.settings_btn.clicked.connect(lambda: self.stack.setCurrentIndex(6))
        self.sidebar.about_btn.clicked.connect(lambda: self.stack.setCurrentIndex(7))
        self.games_page.game_selected.connect(self.open_game)

        # ---------------- Bottom Status Bar ----------------
        self.status = StatusBar()
        self.top_bar.setFixedHeight(70)
        self.status.setFixedHeight(40)
        # Add Layouts
        main_layout.addWidget(self.top_bar)
        main_layout.addLayout(middle_layout, 1)
        main_layout.addWidget(self.status)
    def open_game(self, game_name):

        if game_name == "Snake":
            game = SnakeGame()

        elif game_name == "Racing":
            game = RacingGame()

        elif game_name == "Flappy Bird":
            game = FlappyGame()

        elif game_name == "Fruit Ninja":
            game = FruitNinjaGame()

        elif game_name == "Space Shooter":
            game = SpaceShooterGame()

        else:
            return

        self.play_game_page.game_window.show_game(game)
        self.home_page.update_card(
            "🎮 Current Game",
            game_name
        )
        self.stack.setCurrentWidget(self.play_game_page)