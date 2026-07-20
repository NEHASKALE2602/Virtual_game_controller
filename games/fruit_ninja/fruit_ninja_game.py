import math
import random

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPen
)
from PySide6.QtWidgets import QWidget

from controller.controller_manager import controller


class FruitNinjaGame(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fruit Ninja")
        self.setMinimumSize(1100, 700)
        self.setFocusPolicy(Qt.StrongFocus)

        # -----------------------------
        # Game Timer
        # -----------------------------

        self.timer = QTimer()

        self.timer.timeout.connect(self.update_game)

        self.timer.start(16)

        self.reset_game()

    # ==========================================================
    # RESET GAME
    # ==========================================================

    def reset_game(self):

        # -----------------------------
        # Score
        # -----------------------------

        self.score = 0

        self.combo = 0

        self.high_score = 0

        # -----------------------------
        # Fruits
        # -----------------------------

        self.fruits = []

        self.sliced_fruits = []

        self.particles = []

        self.slice_effects = []

        # -----------------------------
        # Spawn
        # -----------------------------

        self.spawn_counter = 0

        self.spawn_delay = 45

        # -----------------------------
        # Hand Position
        # -----------------------------

        self.hand_x = self.width() // 2

        self.hand_y = self.height() // 2

        self.previous_x = self.hand_x

        self.previous_y = self.hand_y

        # -----------------------------
        # Slice Trail
        # -----------------------------

        self.trail = []

        self.max_trail = 12

        # -----------------------------
        # Gesture
        # -----------------------------

        self.current_gesture = "NONE"

        # -----------------------------
        # Fruit Emojis
        # -----------------------------

        self.fruit_icons = [

            "🍎",

            "🍊",

            "🍉",

            "🍌",

            "🍇",

            "🍓",

            "🍍",

            "🥝"

        ]
        self.missed_fruits = 0
        self.max_missed = 10

        self.game_over = False
            # ==========================================================
    # SPAWN FRUITS
    # ==========================================================

    def spawn_fruit(self):

        # Easy → Medium → Hard

        if self.score < 10:

            count = 1

        elif self.score < 25:

            count = random.randint(1, 2)

        else:

            count = random.randint(2, 3)

        for _ in range(count):

            side = random.choice(["left", "right"])

            if side == "left":

                start_x = random.randint(120, 260)

                vx = random.uniform(2.0, 4.5)

            else:

                start_x = random.randint(self.width() - 260, self.width() - 120)

                vx = random.uniform(-4.5, -2.0)

            fruit = {

                "x": start_x,

                "y": self.height() + 60,

                "vx": vx,

                "vy": random.uniform(-19.5, -17.0),

                "gravity": 0.38,

                "radius": 36,

                "rotation": 0,

                "rotation_speed": random.uniform(-7, 7),

                "emoji": random.choice(self.fruit_icons),

                "sliced": False

            }

            self.fruits.append(fruit)

    # ==========================================================
    # UPDATE FRUITS
    # ==========================================================

    def update_fruits(self):

        remove = []

        for fruit in self.fruits:

            fruit["x"] += fruit["vx"]

            fruit["y"] += fruit["vy"]

            fruit["vy"] += fruit["gravity"]

            fruit["rotation"] += fruit["rotation_speed"]

            if fruit["y"] > self.height() + 100:

                    remove.append(fruit)

                    self.combo = 0

                    self.missed_fruits += 1

                    if self.missed_fruits >= self.max_missed:

                            self.game_over = True

        for fruit in remove:

            if fruit in self.fruits:

                self.fruits.remove(fruit)
                    # ==========================================================
    # UPDATE GAME
    # ==========================================================

    def update_game(self):
        if self.game_over:
            self.update()
            return

        # -----------------------------------------
        # Get Index Finger Position
        # -----------------------------------------

        x, y = controller.get_hand_position()

        if x != 0:

            self.previous_x = self.hand_x
            self.previous_y = self.hand_y

            self.hand_x = int(x * self.width() / 640)
            self.hand_y = int(y * self.height() / 480)

        # -----------------------------------------
        # Save Slice Trail
        # -----------------------------------------

        self.trail.append((self.hand_x, self.hand_y))

        if len(self.trail) > self.max_trail:

            self.trail.pop(0)

        # -----------------------------------------
        # Spawn Fruits
        # -----------------------------------------

        self.spawn_counter += 1

        if self.spawn_counter >= self.spawn_delay:

            self.spawn_counter = 0

            self.spawn_fruit()

        # -----------------------------------------
        # Update Fruits
        # -----------------------------------------

        self.update_fruits()

        # -----------------------------------------
        # Slice Fruits
        # -----------------------------------------

        remove = []

        for fruit in self.fruits:

            distance = math.sqrt(

                (self.hand_x - fruit["x"]) ** 2 +

                (self.hand_y - fruit["y"]) ** 2

            )

            if distance < fruit["radius"]:

                self.score += 1

                self.combo += 1

                self.high_score = max(self.high_score, self.score)

                fruit["sliced"] = True

                # Left Half

                self.sliced_fruits.append({

                    "x": fruit["x"],

                    "y": fruit["y"],

                    "vx": -4,

                    "vy": -4,

                    "gravity": 0.35,

                    "emoji": "◐"

                })

                # Right Half

                self.sliced_fruits.append({

                    "x": fruit["x"],

                    "y": fruit["y"],

                    "vx": 4,

                    "vy": -4,

                    "gravity": 0.35,

                    "emoji": "◑"

                })

                # Particles

                for _ in range(18):

                    self.particles.append({

                        "x": fruit["x"],

                        "y": fruit["y"],

                        "vx": random.uniform(-5, 5),

                        "vy": random.uniform(-5, 5),

                        "life": 25

                    })

                remove.append(fruit)

        for fruit in remove:

            if fruit in self.fruits:

                self.fruits.remove(fruit)

        # -----------------------------------------
        # Update Split Fruits
        # -----------------------------------------

        dead = []

        for part in self.sliced_fruits:

            part["x"] += part["vx"]

            part["y"] += part["vy"]

            part["vy"] += part["gravity"]

            if part["y"] > self.height() + 80:

                dead.append(part)

        for part in dead:

            self.sliced_fruits.remove(part)

        # -----------------------------------------
        # Update Particles
        # -----------------------------------------

        dead = []

        for particle in self.particles:

            particle["x"] += particle["vx"]

            particle["y"] += particle["vy"]

            particle["life"] -= 1

            if particle["life"] <= 0:

                dead.append(particle)

        for particle in dead:

            self.particles.remove(particle)

        self.update()
        # ==========================================================
    # PAINT GAME
    # ==========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        # ======================================================
        # Background
        # ======================================================

        painter.fillRect(self.rect(), QColor(18, 18, 32))

        # ======================================================
        # Score
        # ======================================================

        painter.setPen(Qt.white)

        font = QFont("Segoe UI", 16, QFont.Bold)

        painter.setFont(font)

        painter.drawText(25, 35, f"Score : {self.score}")

        painter.drawText(25, 65, f"High Score : {self.high_score}")

        painter.drawText(25, 95, f"Combo : {self.combo}")

        # ======================================================
        # Title
        # ======================================================

        title = QFont("Segoe UI", 24, QFont.Bold)

        painter.setFont(title)

        painter.setPen(QColor(0, 220, 255))

        painter.drawText(
            self.rect(),
            Qt.AlignTop | Qt.AlignHCenter,
            "FRUIT NINJA"
        )

        # ======================================================
        # Slice Trail
        # ======================================================

        if len(self.trail) > 1:

            for i in range(len(self.trail) - 1):

                alpha = int(255 * (i + 1) / len(self.trail))

                pen = QPen(QColor(0, 220, 255, alpha))

                pen.setWidth(6)

                pen.setCapStyle(Qt.RoundCap)

                painter.setPen(pen)

                painter.drawLine(

                    self.trail[i][0],
                    self.trail[i][1],

                    self.trail[i + 1][0],
                    self.trail[i + 1][1]

                )

        # ======================================================
        # Fruits
        # ======================================================

        fruit_font = QFont()

        fruit_font.setPointSize(34)

        painter.setFont(fruit_font)

        painter.setPen(Qt.white)

        for fruit in self.fruits:

            painter.drawText(

                int(fruit["x"]),

                int(fruit["y"]),

                fruit["emoji"]

            )

        # ======================================================
        # Split Fruits
        # ======================================================

        split_font = QFont()

        split_font.setPointSize(30)

        painter.setFont(split_font)

        for part in self.sliced_fruits:

            painter.drawText(

                int(part["x"]),

                int(part["y"]),

                part["emoji"]

            )

        # ======================================================
        # Particles
        # ======================================================

        painter.setPen(Qt.NoPen)

        for particle in self.particles:

            painter.setBrush(QColor(255, 240, 120))

            painter.drawEllipse(

                int(particle["x"]),

                int(particle["y"]),

                5,

                5

            )

        # ======================================================
        # Finger Cursor
        # ======================================================

        painter.setBrush(QColor(0, 255, 255))

        painter.drawEllipse(

            self.hand_x - 10,

            self.hand_y - 10,

            20,

            20

        )
                # ======================================================
        # GAME OVER SCREEN
        # ======================================================

        if self.game_over:

            painter.setBrush(QColor(0, 0, 0, 180))
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.rect())

            painter.setPen(Qt.white)

            title_font = QFont("Segoe UI", 34, QFont.Bold)
            painter.setFont(title_font)

            painter.drawText(
                self.rect(),
                Qt.AlignCenter,
                "GAME OVER"
            )

            score_font = QFont("Segoe UI", 18, QFont.Bold)
            painter.setFont(score_font)

            painter.drawText(
                self.width() // 2 - 80,
                self.height() // 2 + 60,
                f"Score : {self.score}"
            )

            painter.drawText(
                self.width() // 2 - 110,
                self.height() // 2 + 100,
                f"Missed Fruits : {self.missed_fruits}/10"
            )

    # ==========================================================
    # WINDOW EVENTS
    # ==========================================================

    def resizeEvent(self, event):

        super().resizeEvent(event)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:

            self.close()

    def closeEvent(self, event):

        if self.timer.isActive():

            self.timer.stop()

        event.accept()
    # ==========================================================
# END OF FILE
# ==========================================================

    # Optional Restart Method

    def restart_game(self):

        self.reset_game()

    # ==========================================================
    # OPTIONAL MOUSE SUPPORT (Testing Without Camera)
    # ==========================================================

    def mouseMoveEvent(self, event):

        self.hand_x = event.position().x()

        self.hand_y = event.position().y()

    # ==========================================================
    # OPTIONAL FPS LIMIT
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
    # END
    # ==========================================================