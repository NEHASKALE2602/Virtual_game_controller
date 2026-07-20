from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFrame
)
from controller.analytics_manager import analytics


class StatCard(QFrame):

    def __init__(self, title, value):

        super().__init__()

        self.setObjectName("analyticsCard")
        self.setFixedHeight(70)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(2)

        self.title = QLabel(title)
        self.title.setObjectName("analyticsTitle")
        self.title.setAlignment(Qt.AlignCenter)

        self.value = QLabel(value)
        self.value.setObjectName("analyticsValue")
        self.value.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title)
        layout.addWidget(self.value)



class AnalyticsPage(QWidget):

    def __init__(self):

        super().__init__()

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(30, 25, 30, 25)

        main_layout.setSpacing(25)

        # ==========================================
        # PAGE TITLE
        # ==========================================

        title = QLabel("📊 ANALYTICS")

        title.setObjectName("pageTitle")

        title.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title)

        # ==========================================
        # MAIN TWO PANELS
        # ==========================================

        self.content_layout = QHBoxLayout()

        self.content_layout.setSpacing(25)

        main_layout.addLayout(self.content_layout)

        # ==========================================
        # LEFT PANEL
        # ==========================================

        self.left_panel = QFrame()

        self.left_panel.setObjectName("analyticsPanel")

        self.left_layout = QVBoxLayout(self.left_panel)

        self.left_layout.setContentsMargins(20,20,20,20)

        self.left_layout.setSpacing(10)

        self.content_layout.addWidget(self.left_panel,1)

       
        # ==========================================
        # RIGHT PANEL
        # ==========================================

        self.right_panel = QFrame()

        self.right_panel.setObjectName("analyticsPanel")

        self.right_layout = QVBoxLayout(self.right_panel)

        self.right_layout.setContentsMargins(20,20,20,20)

        self.right_layout.setSpacing(10)

        self.content_layout.addWidget(self.right_panel,1)

        # ==========================================
# RIGHT PANEL TITLE
# ==========================================

        right_title = QLabel("📈 LIVE GAME STATISTICS")

        right_title.setObjectName("panelTitle")

        right_title.setAlignment(Qt.AlignCenter)

        self.right_layout.addWidget(right_title)

# ==========================================
# CURRENT GAME
# ==========================================

        self.current_game = StatCard(
            "🎮 Current Game",
            "None"
        )

        self.right_layout.addWidget(self.current_game)

# ==========================================
# CURRENT SCORE
# ==========================================

        self.current_score = StatCard(
            "🎯 Current Score",
            "0"
        )

        self.right_layout.addWidget(self.current_score)

# ==========================================
# HIGH SCORE
# ==========================================

        self.current_high = StatCard(
            "🏆 High Score",
            "0"
        )

        self.right_layout.addWidget(self.current_high)

# ==========================================
# GAME STATUS
# ==========================================

        self.game_status = StatCard(
            "⚡ Game Status",
            "Waiting"
        )

        self.right_layout.addWidget(self.game_status)

# ==========================================
# TIME PLAYED
# ==========================================

        self.time_played = StatCard(
            "⏱ Time Played",
            "00:00"
        )

        self.right_layout.addWidget(self.time_played)

# ==========================================
# CURRENT GESTURE
# ==========================================

        self.current_gesture = StatCard(
            "✋ Current Gesture",
            "NO HAND"
        )

        self.right_layout.addWidget(self.current_gesture)

        self.right_layout.addStretch()
        
        left_title = QLabel("🏆 GAME HIGH SCORES")

        left_title.setObjectName("panelTitle")

        left_title.setAlignment(Qt.AlignCenter)

        self.left_layout.addWidget(left_title)

# ----------------------------------------------------------
# Fruit Ninja
# ----------------------------------------------------------

        self.fruit_card = StatCard(

            "🍎 Fruit Ninja",

            "High Score : 0"

        )

        self.left_layout.addWidget(self.fruit_card)

# ----------------------------------------------------------
# Snake
# ----------------------------------------------------------

        self.snake_card = StatCard(

            "🐍 Snake",

            "High Score : 0"

        )

        self.left_layout.addWidget(self.snake_card)

# ----------------------------------------------------------
# Racing
# ----------------------------------------------------------

        self.racing_card = StatCard(

            "🚗 Racing",

            "Best Time : 00:00"

        )

        self.left_layout.addWidget(self.racing_card)

# ----------------------------------------------------------
# Flappy Bird
# ----------------------------------------------------------

        self.flappy_card = StatCard(

            "🐦 Flappy Bird",

            "High Score : 0"

        )

        self.left_layout.addWidget(self.flappy_card)

# ----------------------------------------------------------
# Space Shooter
# ----------------------------------------------------------

        self.space_card = StatCard(

            "🚀 Space Shooter",

            "High Score : 0"

        )

        self.left_layout.addWidget(self.space_card)

        self.left_layout.addStretch()
        # ==========================================
# AUTO REFRESH
# ==========================================

        self.timer = QTimer()

        self.timer.timeout.connect(self.refresh_data)

        self.timer.start(200)
        # ==========================================================
    # UPDATE LIVE GAME DATA
    # ==========================================================
       
    def update_game_data(
        self,
        game_name,
        score,
        high_score,
        status,
        time_played,
        gesture
    ):

        self.current_game.value.setText(str(game_name))
        self.current_score.value.setText(str(score))
        self.current_high.value.setText(str(high_score))
        self.game_status.value.setText(str(status))
        self.time_played.value.setText(str(time_played))
        self.current_gesture.value.setText(str(gesture))

        if game_name == "Fruit Ninja":
            self.fruit_card.value.setText(f"High Score : {high_score}")

        elif game_name == "Snake":
            self.snake_card.value.setText(f"High Score : {high_score}")

        elif game_name == "Racing":
            self.racing_card.value.setText(f"Best Time : {high_score}")

        elif game_name == "Flappy Bird":
            self.flappy_card.value.setText(f"High Score : {high_score}")

        elif game_name == "Space Shooter":
            self.space_card.value.setText(f"High Score : {high_score}")


    # ==========================================================
    # REFRESH ANALYTICS
    # ==========================================================

    def refresh_data(self):

        self.current_game.value.setText(str(analytics.current_game))
        self.current_score.value.setText(str(analytics.current_score))
        self.current_high.value.setText(str(analytics.high_score))
        self.game_status.value.setText(str(analytics.status))
        self.time_played.value.setText(str(analytics.time_played))
        self.current_gesture.value.setText(str(analytics.gesture))

        self.fruit_card.value.setText(
            f"High Score : {analytics.high_scores['Fruit Ninja']}"
        )

        self.snake_card.value.setText(
            f"High Score : {analytics.high_scores['Snake']}"
        )

        self.racing_card.value.setText(
            f"Best Time : {analytics.high_scores['Racing']}"
        )

        self.flappy_card.value.setText(
            f"High Score : {analytics.high_scores['Flappy Bird']}"
        )

        self.space_card.value.setText(
            f"High Score : {analytics.high_scores['Space Shooter']}"
        )
 