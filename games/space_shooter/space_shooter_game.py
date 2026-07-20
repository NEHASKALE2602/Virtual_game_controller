import random
import math

from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import (
    QPainter,
    QColor,
    QFont,
    QPen
)
from PySide6.QtWidgets import QWidget

from controller.controller_manager import controller


class SpaceShooterGame(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(900, 600)
        self.setFocusPolicy(Qt.StrongFocus)

        # ============================================
        # Timer
        # ============================================

        self.timer = QTimer()

        self.timer.timeout.connect(self.update_game)

        self.timer.start(16)

        # ============================================
        # Player
        # ============================================

        self.player_x = 450
        self.player_y = 520

        self.target_x = 450
        self.target_y = 520

        self.ship_width = 60
        self.ship_height = 70

        self.move_speed = 0.18

        # ============================================
        # Camera Size
        # ============================================

        self.camera_width = 640
        self.camera_height = 480

        # ============================================
        # Game
        # ============================================

        self.score = 0
        self.high_score = 0

        self.lives = 3

        self.game_over = False

        self.fire_delay = 0

        # ============================================
        # Objects
        # ============================================

        self.bullets = []

        self.enemies = []

        self.explosions = []

        self.stars = []

        # ============================================
        # Difficulty
        # ============================================

        self.enemy_speed = 4

        self.spawn_counter = 0

        # ============================================
        # Background Stars
        # ============================================

        for i in range(120):

            self.stars.append({

                "x": random.randint(0, 900),

                "y": random.randint(0, 600),

                "size": random.randint(1, 3),

                "speed": random.uniform(1, 4)

            })
                # ==========================================================
    # UPDATE GAME
    # ==========================================================

    def update_game(self):

        if self.game_over:
            self.update()
            return

        # ======================================================
        # Camera Hand Position
        # ======================================================

        hand_x, hand_y = controller.get_hand_position()

        # ------------------------------------------------------
        # Map Camera (640x480) -> Game Window
        # ------------------------------------------------------

        if hand_x != 0 or hand_y != 0:

            self.target_x = (hand_x / self.camera_width) * self.width()

            self.target_y = (hand_y / self.camera_height) * self.height()

            # Keep ship inside screen

            margin = 35

            self.target_x = max(
                margin,
                min(self.width() - margin, self.target_x)
            )

            self.target_y = max(
                margin,
                min(self.height() - margin, self.target_y)
            )

        # ======================================================
        # Smooth Movement
        # ======================================================

        self.player_x += (
            self.target_x - self.player_x
        ) * self.move_speed

        self.player_y += (
            self.target_y - self.player_y
        ) * self.move_speed

        # ======================================================
        # Auto Fire
        # ======================================================

        gesture = controller.get_gesture()

        if self.fire_delay > 0:

            self.fire_delay -= 1

        if gesture == "POINTING" and self.fire_delay == 0:

            self.bullets.append({

                "x": self.player_x,

                "y": self.player_y - 30,

                "speed": 14

            })

            self.fire_delay = 8

        # ======================================================
        # Background Stars
        # ======================================================

        for star in self.stars:

            star["y"] += star["speed"]

            if star["y"] > self.height():

                star["y"] = 0

                star["x"] = random.randint(0, self.width())

        # ======================================================
        # Move Bullets
        # ======================================================

        for bullet in self.bullets[:]:

            bullet["y"] -= bullet["speed"]

            if bullet["y"] < -20:

                self.bullets.remove(bullet)
        
                        # ======================================================
        # Spawn Enemies
        # ======================================================

        self.spawn_counter += 1

        if self.spawn_counter >= 35:

            self.spawn_counter = 0

            self.enemies.append({

                "x": random.randint(40, self.width() - 40),

                "y": -60,

                "speed": self.enemy_speed,

                "hp": 1,

                "rotation": 0

            })

        # ======================================================
        # Move Enemies
        # ======================================================

        for enemy in self.enemies[:]:

            enemy["y"] += enemy["speed"]

            enemy["rotation"] += 5

            # ----------------------------------------------
            # Enemy Missed
            # ----------------------------------------------

            if enemy["y"] > self.height() + 60:

                self.enemies.remove(enemy)

                self.lives -= 1

                if self.lives <= 0:

                    self.game_over = True

                    if self.score > self.high_score:

                        self.high_score = self.score

                continue

            # ----------------------------------------------
            # Ship Collision
            # ----------------------------------------------

            dx = enemy["x"] - self.player_x
            dy = enemy["y"] - self.player_y

            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 45:

                self.enemies.remove(enemy)

                self.lives -= 1

                self.explosions.append({

                    "x": enemy["x"],

                    "y": enemy["y"],

                    "radius": 10,

                    "alpha": 255

                })

                if self.lives <= 0:

                    self.game_over = True

                    if self.score > self.high_score:

                        self.high_score = self.score

                continue

            # ----------------------------------------------
            # Bullet Collision
            # ----------------------------------------------

            for bullet in self.bullets[:]:

                dx = bullet["x"] - enemy["x"]
                dy = bullet["y"] - enemy["y"]

                if math.sqrt(dx * dx + dy * dy) < 35:

                    if bullet in self.bullets:

                        self.bullets.remove(bullet)

                    if enemy in self.enemies:

                        self.enemies.remove(enemy)

                    self.score += 10

                    self.explosions.append({

                        "x": enemy["x"],

                        "y": enemy["y"],

                        "radius": 10,

                        "alpha": 255

                    })

                    break

        # ======================================================
        # Explosion Animation
        # ======================================================

        for explosion in self.explosions[:]:

            explosion["radius"] += 4

            explosion["alpha"] -= 18

            if explosion["alpha"] <= 0:

                self.explosions.remove(explosion)

        # ======================================================
        # Difficulty Increase
        # ======================================================

        self.enemy_speed = 4 + (self.score // 200) * 0.5
        self.update()
            # ==========================================================
    # PAINT GAME
    # ==========================================================

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # ======================================================
        # Space Background
        # ======================================================

        painter.fillRect(self.rect(), QColor(8, 12, 30))

        # ======================================================
        # Stars
        # ======================================================

        painter.setPen(Qt.NoPen)

        for star in self.stars:

            painter.setBrush(QColor(255, 255, 255))

            painter.drawEllipse(

                int(star["x"]),
                int(star["y"]),

                star["size"],
                star["size"]

            )

        # ======================================================
        # Bullets
        # ======================================================

        painter.setBrush(QColor(0, 255, 255))

        for bullet in self.bullets:

            painter.drawRoundedRect(

                int(bullet["x"]) - 3,
                int(bullet["y"]),

                6,
                22,

                3,
                3

            )

        # ======================================================
        # Enemies
        # ======================================================

        for enemy in self.enemies:

            painter.save()

            painter.translate(

                enemy["x"],
                enemy["y"]

            )

            painter.rotate(enemy["rotation"])

            painter.setBrush(QColor(255, 70, 70))

            painter.setPen(Qt.NoPen)

            painter.drawEllipse(

                -22,
                -22,

                44,
                44

            )

            painter.setBrush(Qt.white)

            painter.drawEllipse(-10, -8, 6, 6)
            painter.drawEllipse(4, -8, 6, 6)

            painter.restore()

        # ======================================================
        # Explosions
        # ======================================================

        painter.setPen(Qt.NoPen)

        for explosion in self.explosions:

            painter.setBrush(

                QColor(

                    255,
                    180,
                    0,

                    explosion["alpha"]

                )

            )

            painter.drawEllipse(

                explosion["x"] - explosion["radius"],

                explosion["y"] - explosion["radius"],

                explosion["radius"] * 2,

                explosion["radius"] * 2

            )

        # ======================================================
        # Player Ship
        # ======================================================

        painter.save()

        painter.translate(

            self.player_x,

            self.player_y

        )

        painter.setPen(Qt.NoPen)

        # Main Body

        painter.setBrush(QColor(0, 220, 255))

        painter.drawPolygon([

            QPointF(0, -35),

            QPointF(-22, 25),

            QPointF(0, 10),

            QPointF(22, 25)

        ])

        # Cockpit

        painter.setBrush(QColor(120, 240, 255))

        painter.drawEllipse(

            -8,
            -12,

            16,
            20

        )

        # Wings

        painter.setBrush(QColor(80, 170, 255))

        painter.drawRect(-30, 5, 12, 8)

        painter.drawRect(18, 5, 12, 8)

        painter.restore()

        # ======================================================
        # Score
        # ======================================================

        painter.setPen(Qt.white)

        font = QFont("Segoe UI", 16, QFont.Bold)

        painter.setFont(font)

        painter.drawText(

            20,
            35,

            f"Score : {self.score}"

        )

        painter.drawText(

            20,
            65,

            f"High Score : {self.high_score}"

        )

        # ======================================================
        # Lives
        # ======================================================

        painter.setPen(Qt.NoPen)

        for i in range(self.lives):

            painter.setBrush(QColor(255, 60, 60))

            painter.drawEllipse(

                self.width() - 40 - (i * 35),

                20,

                22,

                22

            )

        # ======================================================
        # Game Over
        # ======================================================

        if self.game_over:

            painter.fillRect(

                self.rect(),

                QColor(0, 0, 0, 170)

            )

            title = QFont("Segoe UI", 34, QFont.Bold)

            painter.setFont(title)

            painter.setPen(Qt.white)

            painter.drawText(

                self.rect(),

                Qt.AlignCenter,

                "GAME OVER"

            )

            small = QFont("Segoe UI", 18)

            painter.setFont(small)

            painter.drawText(

                self.width() // 2 - 70,

                self.height() // 2 + 60,

                f"Score : {self.score}"

            )

            painter.drawText(

                self.width() // 2 - 95,

                self.height() // 2 + 95,

                "Press R : Restart"

            )

            painter.drawText(

                self.width() // 2 - 85,

                self.height() // 2 + 125,

                "Press ESC : Exit"

            )
                # ==========================================================
    # KEYBOARD CONTROLS
    # ==========================================================

    def keyPressEvent(self, event):

        # ---------------------------------------
        # Restart
        # ---------------------------------------

        if event.key() == Qt.Key_R and self.game_over:

            self.score = 0

            self.lives = 3

            self.enemy_speed = 4

            self.spawn_counter = 0

            self.game_over = False

            self.player_x = self.width() // 2
            self.player_y = self.height() - 80

            self.target_x = self.player_x
            self.target_y = self.player_y

            self.bullets.clear()
            self.enemies.clear()
            self.explosions.clear()

            return

        # ---------------------------------------
        # Exit
        # ---------------------------------------

        if event.key() == Qt.Key_Escape:

            self.close()

    # ==========================================================
    # SHOW EVENT
    # ==========================================================

    def showEvent(self, event):

        self.timer.start(16)

        super().showEvent(event)

    # ==========================================================
    # HIDE EVENT
    # ==========================================================

    def hideEvent(self, event):

        self.timer.stop()

        super().hideEvent(event)

    # ==========================================================
    # CLOSE EVENT
    # ==========================================================

    def closeEvent(self, event):

        if self.timer.isActive():

            self.timer.stop()

        event.accept()
           