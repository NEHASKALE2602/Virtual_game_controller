import random
import math

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QFont
from PySide6.QtWidgets import QWidget

from controller.controller_manager import controller


class SpaceShooterGame(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Space Shooter")

        self.setMinimumSize(1000, 700)
        self.setFocusPolicy(Qt.StrongFocus)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

        self.reset_game()

    # =====================================================
    # RESET GAME
    # =====================================================

    def reset_game(self):

        self.score = 0

        self.health = 5

        self.ship_x = self.width() // 2

        self.ship_y = self.height() - 120

        self.target_x = self.ship_x

        self.previous_x = self.ship_x

        self.bullets = []

        self.enemies = []

        self.explosions = []

        self.stars = []

        self.spawn_counter = 0

        self.fire_counter = 0

        self.direction_x = 0

        # -------------------------
        # Background Stars
        # -------------------------

        for _ in range(180):

            self.stars.append({

                "x": random.randint(0, self.width()),

                "y": random.randint(0, self.height()),

                "speed": random.randint(2, 8),

                "size": random.randint(1, 3)

            })
        # =====================================================
    # Spawn Enemy
    # =====================================================

    def spawn_enemy(self):

        enemy = {

            "x": random.randint(60, self.width() - 60),

            "y": -80,

            "radius": 28,

            "speed": random.randint(3, 6)

        }

        self.enemies.append(enemy)

    # =====================================================
    # Fire Bullet
    # =====================================================

    def fire_bullet(self):

        dx = self.direction_x

        bullet = {

            "x": self.ship_x,

            "y": self.ship_y - 35,

            "dx": dx,

            "dy": -15,

            "radius": 5

        }

        self.bullets.append(bullet)

    # =====================================================
    # Update Game
    # =====================================================

    def update_game(self):

        # -----------------------------------------
        # Finger Position
        # -----------------------------------------

        x, y = controller.get_hand_position()

        if x != 0:

            self.target_x = int(x * self.width() / 640)

        # -----------------------------------------
        # Smooth Ship Movement
        # -----------------------------------------

        self.ship_x += (self.target_x - self.ship_x) * 0.20

        self.direction_x = self.ship_x - self.previous_x

        self.previous_x = self.ship_x

        # -----------------------------------------
        # Auto Fire
        # -----------------------------------------

        self.fire_counter += 1

        if self.fire_counter >= 8:

            self.fire_counter = 0

            self.fire_bullet()

        # -----------------------------------------
        # Spawn Enemy
        # -----------------------------------------

        self.spawn_counter += 1

        if self.spawn_counter >= 35:

            self.spawn_counter = 0

            self.spawn_enemy()

        # -----------------------------------------
        # Update Stars
        # -----------------------------------------

        for star in self.stars:

            star["y"] += star["speed"]

            if star["y"] > self.height():

                star["y"] = 0

                star["x"] = random.randint(0, self.width())

        # -----------------------------------------
        # Update Bullets
        # -----------------------------------------

        remove_bullets = []

        for bullet in self.bullets:

            bullet["x"] += bullet["dx"]

            bullet["y"] += bullet["dy"]

            if bullet["y"] < -20:

                remove_bullets.append(bullet)

        for bullet in remove_bullets:

            if bullet in self.bullets:

                self.bullets.remove(bullet)

        # -----------------------------------------
        # Update Enemies
        # -----------------------------------------

        remove_enemy = []

        for enemy in self.enemies:

            enemy["y"] += enemy["speed"]

            if enemy["y"] > self.height() + 80:

                remove_enemy.append(enemy)

        for enemy in remove_enemy:

            if enemy in self.enemies:

                self.enemies.remove(enemy)

        self.update()
        # =====================================================
    # Paint Game
    # =====================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        # ==========================================
        # Background
        # ==========================================

        painter.fillRect(self.rect(), QColor(5, 5, 20))

        # ==========================================
        # Stars
        # ==========================================

        painter.setPen(Qt.NoPen)

        for star in self.stars:

            painter.setBrush(QColor(255, 255, 255))

            painter.drawEllipse(

                int(star["x"]),
                int(star["y"]),
                star["size"],
                star["size"]

            )

        # ==========================================
        # Bullets
        # ==========================================

        painter.setBrush(QColor(255, 255, 0))

        for bullet in self.bullets:

            painter.drawEllipse(

                int(bullet["x"] - bullet["radius"]),
                int(bullet["y"] - bullet["radius"]),
                bullet["radius"] * 2,
                bullet["radius"] * 2

            )

        # ==========================================
        # Enemies
        # ==========================================

        for enemy in self.enemies:

            painter.setBrush(QColor(255, 70, 70))

            painter.drawEllipse(

                int(enemy["x"] - enemy["radius"]),
                int(enemy["y"] - enemy["radius"]),
                enemy["radius"] * 2,
                enemy["radius"] * 2

            )

            painter.setBrush(Qt.black)

            painter.drawEllipse(
                int(enemy["x"] - 12),
                int(enemy["y"] - 8),
                8,
                8
            )

            painter.drawEllipse(
                int(enemy["x"] + 4),
                int(enemy["y"] - 8),
                8,
                8
            )

            painter.setBrush(QColor(255, 255, 255))

            painter.drawEllipse(
                int(enemy["x"] - 4),
                int(enemy["y"] + 8),
                8,
                8
            )

        # ==========================================
        # Spaceship
        # ==========================================

        painter.setBrush(QColor(0, 220, 255))

        ship_points = [

            (int(self.ship_x), int(self.ship_y - 35)),

            (int(self.ship_x - 28), int(self.ship_y + 30)),

            (int(self.ship_x), int(self.ship_y + 10)),

            (int(self.ship_x + 28), int(self.ship_y + 30))

        ]

        from PySide6.QtCore import QPoint

        painter.drawPolygon(

            QPoint(*ship_points[0]),
            QPoint(*ship_points[1]),
            QPoint(*ship_points[2]),
            QPoint(*ship_points[3])

        )

        # ==========================================
        # Engine Flame
        # ==========================================

        painter.setBrush(QColor(255, 180, 0))

        painter.drawEllipse(

            int(self.ship_x - 8),
            int(self.ship_y + 28),
            16,
            26

        )
            # ==========================================
        # HUD
        # ==========================================

        painter.setPen(Qt.white)

        font = QFont()
        font.setPointSize(16)
        font.setBold(True)

        painter.setFont(font)

        painter.drawText(20, 35, f"Score : {self.score}")
        painter.drawText(20, 65, f"Health : {self.health}")

        painter.drawText(
            self.width() - 230,
            35,
            "INDEX FINGER AIM"
        )

        painter.drawText(
            self.width() - 230,
            65,
            "AUTO SHOOT"
        )

        # ==========================================
        # Finger Target
        # ==========================================

        painter.setPen(Qt.NoPen)

        painter.setBrush(QColor(0, 255, 120))

        painter.drawEllipse(

            int(self.target_x - 8),
            int(self.ship_y - 110),
            16,
            16

        )

    # =====================================================
    # Resize
    # =====================================================

    def resizeEvent(self, event):

        super().resizeEvent(event)

    # =====================================================
    # Keyboard
    # =====================================================

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:

            self.close()

    # =====================================================
    # Close
    # =====================================================

    def closeEvent(self, event):

        if self.timer.isActive():

            self.timer.stop()

        event.accept()