import random

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QFont
from PySide6.QtWidgets import QWidget

from controller.controller_manager import controller
from controller.analytics_manager import analytics
from controller.controller_manager import controller


class RacingGame(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Gesture Racing")

        self.setMinimumSize(900, 600)
        self.setFocusPolicy(Qt.StrongFocus)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)      # 60 FPS

        self.reset_game()

    # ==========================================================
    # Reset Game
    # ==========================================================

    def reset_game(self):

        # Road

        self.road_width = 420

        self.lane_width = self.road_width // 3

        self.road_x = (self.width() - self.road_width) // 2

        self.line_offset = 0

        # Player

        self.player_lane = 1

        self.player_speed = 0

        self.max_speed = 18

        self.distance = 0

        self.score = 0

        # Gesture

        self.current_gesture = "NONE"

        # Nitro

        self.nitro = False

        self.nitro_timer = 0

        # Enemy Cars

        self.enemy_cars = []

        self.spawn_counter = 0
            # ==========================================================
    # Spawn Enemy Car
    # ==========================================================

    def spawn_enemy(self):

        lane = random.randint(0, 2)

        x = self.road_x + lane * self.lane_width + self.lane_width // 2

        enemy = {

            "lane": lane,

            "x": x,

            "y": -120,

            "speed": random.randint(8, 14),

            "color": random.choice([
                QColor(255, 80, 80),
                QColor(80, 180, 255),
                QColor(255, 220, 80),
                QColor(120, 255, 120),
                QColor(255, 120, 255)
            ])

        }

        self.enemy_cars.append(enemy)

    # ==========================================================
    # Update Game
    # ==========================================================

    def update_game(self):

        self.current_gesture = controller.get_gesture()

        # ---------------------------------------------
        # Gesture Controls
        # ---------------------------------------------

        if self.current_gesture == "POINTING":

            if self.player_speed < self.max_speed:

                self.player_speed += 0.30

        elif self.current_gesture == "OPEN PALM":

            if self.player_speed > 0:

                self.player_speed -= 0.50

        elif self.current_gesture == "LEFT":

            self.player_lane = max(0, self.player_lane - 1)

        elif self.current_gesture == "RIGHT":

            self.player_lane = min(2, self.player_lane + 1)

        elif self.current_gesture == "FIST":

            self.nitro = True
            self.nitro_timer = 40

        # ---------------------------------------------
        # Nitro
        # ---------------------------------------------

        if self.nitro:

            self.player_speed = self.max_speed + 6

            self.nitro_timer -= 1

            if self.nitro_timer <= 0:

                self.nitro = False

                self.player_speed = self.max_speed

        # ---------------------------------------------
        # Road Animation
        # ---------------------------------------------

        self.line_offset += self.player_speed

        if self.line_offset >= 60:

            self.line_offset = 0

        self.distance += self.player_speed * 0.05

        self.score = int(self.distance)

        # ---------------------------------------------
        # Spawn Enemy
        # ---------------------------------------------

        self.spawn_counter += 1

        if self.spawn_counter > 40:

            self.spawn_counter = 0

            self.spawn_enemy()

        # ---------------------------------------------
        # Move Enemy Cars
        # ---------------------------------------------

        remove = []

        for enemy in self.enemy_cars:

            enemy["y"] += enemy["speed"] + self.player_speed

            if enemy["y"] > self.height() + 120:

                remove.append(enemy)

        for enemy in remove:

            self.enemy_cars.remove(enemy)
        analytics.update(

            game="Racing",

            score=self.score,

            high_score=self.high_score,

            status="Playing",

            time_played="00:00",

            gesture=controller.get_gesture()

        )
        self.update()
        # ==========================================================
    # Paint Game
    # ==========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        # ==================================================
        # Background
        # ==================================================

        painter.fillRect(self.rect(), QColor(20, 20, 30))

        # ==================================================
        # Grass
        # ==================================================

        painter.fillRect(
            0,
            0,
            self.road_x,
            self.height(),
            QColor(30, 120, 30)
        )

        painter.fillRect(
            self.road_x + self.road_width,
            0,
            self.width() - (self.road_x + self.road_width),
            self.height(),
            QColor(30, 120, 30)
        )

        # ==================================================
        # Road
        # ==================================================

        painter.fillRect(
            self.road_x,
            0,
            self.road_width,
            self.height(),
            QColor(45, 45, 45)
        )

        # ==================================================
        # Road Borders
        # ==================================================

        painter.setPen(QColor(255, 255, 255))

        painter.drawLine(
            self.road_x,
            0,
            self.road_x,
            self.height()
        )

        painter.drawLine(
            self.road_x + self.road_width,
            0,
            self.road_x + self.road_width,
            self.height()
        )

        # ==================================================
        # Lane Markings
        # ==================================================

        painter.setPen(QColor(240, 240, 240))

        for lane in range(1, 3):

            x = self.road_x + lane * self.lane_width

            y = -60 + self.line_offset

            while y < self.height():

                painter.drawLine(
                    x,
                    y,
                    x,
                    y + 35
                )

                y += 70

        # ==================================================
        # Player Car
        # ==================================================

        player_x = (
            self.road_x
            + self.player_lane * self.lane_width
            + self.lane_width // 2
            - 25
        )

        player_y = self.height() - 140

        painter.setBrush(QColor(0, 220, 255))
        painter.setPen(Qt.NoPen)

        painter.drawRoundedRect(
            player_x,
            player_y,
            50,
            90,
            12,
            12
        )

        # Wheels

        painter.setBrush(QColor(30, 30, 30))

        painter.drawEllipse(player_x - 6, player_y + 10, 10, 20)
        painter.drawEllipse(player_x + 46, player_y + 10, 10, 20)

        painter.drawEllipse(player_x - 6, player_y + 60, 10, 20)
        painter.drawEllipse(player_x + 46, player_y + 60, 10, 20)

        # Windshield

        painter.setBrush(QColor(180, 240, 255))

        painter.drawRoundedRect(
            player_x + 8,
            player_y + 15,
            34,
            22,
            6,
            6
        )

        # ==================================================
        # Enemy Cars
        # ==================================================

        for enemy in self.enemy_cars:

            painter.setBrush(enemy["color"])

            painter.drawRoundedRect(
                enemy["x"] - 25,
                enemy["y"],
                50,
                90,
                12,
                12
            )
        # ==========================================================
    # Dashboard
    # ==========================================================

        painter.setPen(Qt.white)

        font = QFont()
        font.setPointSize(14)
        font.setBold(True)

        painter.setFont(font)

        painter.drawText(20, 35, f"Score : {self.score}")
        painter.drawText(20, 65, f"Distance : {int(self.distance)} m")
        painter.drawText(20, 95, f"Speed : {int(self.player_speed)}")

        painter.drawText(
            self.width() - 230,
            35,
            f"Gesture : {self.current_gesture}"
        )

        if self.nitro:

            painter.setPen(QColor(255, 255, 0))

            painter.drawText(
                self.width() - 230,
                65,
                "⚡ NITRO BOOST"
            )

        # Instructions

        painter.setPen(QColor(0, 255, 255))

        font = QFont()
        font.setPointSize(11)

        painter.setFont(font)

        painter.drawText(
            self.width() - 320,
            self.height() - 80,
            "☝ POINTING = DRIVE"
        )

        painter.drawText(
            self.width() - 320,
            self.height() - 60,
            "✋ OPEN PALM = STOP"
        )

        painter.drawText(
            self.width() - 320,
            self.height() - 40,
            "👈 LEFT / 👉 RIGHT = STEER"
        )

        painter.drawText(
            self.width() - 320,
            self.height() - 20,
            "✊ FIST = NITRO"
        )

    # ==========================================================
    # Resize
    # ==========================================================

    def resizeEvent(self, event):

        self.road_x = (self.width() - self.road_width) // 2

        super().resizeEvent(event)

    # ==========================================================
    # Keyboard
    # ==========================================================

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:

            self.close()

    # ==========================================================
    # Close
    # ==========================================================

    def closeEvent(self, event):

        if self.timer.isActive():

            self.timer.stop()

        event.accept()