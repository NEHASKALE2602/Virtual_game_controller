import random

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QFont
from PySide6.QtWidgets import QWidget

from controller.controller_manager import controller


class FruitNinjaGame(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fruit Ninja")

        self.setMinimumSize(900, 600)
        self.setFocusPolicy(Qt.StrongFocus)

        # Game Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(30)

        self.reset_game()

    # ==========================================================
    # Reset Game
    # ==========================================================

    def reset_game(self):

        # Score
        self.score = 0
        self.high_score = 0
        self.combo = 0

        # Fruits
        self.fruits = []
        self.sliced_fruits = []

        # Slice Animation
        self.effects = []

        # Spawn Counter
        self.spawn_counter = 0

        # Hand Position
        self.hand_x = self.width() // 2
        self.hand_y = self.height() // 2

        # Gesture
        self.current_gesture = "NONE"

        # Fruit List
        self.fruit_icons = [
            "🍎",
            "🍊",
            "🍉",
            "🍓",
            "🍇",
            "🍌",
            "🥝",
            "🍍"
        ]

    # ==========================================================
    # Spawn Fruits
    # ==========================================================

    def spawn_fruit(self):

        count = random.randint(1, 3)

        for _ in range(count):

            fruit = {

                "x": random.randint(80, self.width() - 80),

                "y": self.height() - random.randint(20, 60),

                "vx": random.randint(-4, 4),

                "vy": random.randint(-22, -18),

                "gravity": 0.45,

                "emoji": random.choice(self.fruit_icons),

                "cut": False

            }

            self.fruits.append(fruit)
        # ==========================================================
    # Update Game
    # ==========================================================

    def update_game(self):

        # ---------------- Hand Position ----------------

        x, y = controller.get_hand_position()

        if x != 0:

            self.hand_x = int(x * self.width() / 640)
            self.hand_y = int(y * self.height() / 480)

        # ---------------- Current Gesture ----------------

        self.current_gesture = controller.get_gesture()

        # ---------------- Spawn Fruits ----------------

        self.spawn_counter += 1

        if self.spawn_counter >= 20:

            self.spawn_counter = 0

            self.spawn_fruit()

        remove = []

        # ---------------- Update Fruits ----------------

        for fruit in self.fruits:

            fruit["x"] += fruit["vx"]

            fruit["vy"] += fruit["gravity"]

            fruit["y"] += fruit["vy"]

            # ==================================================
            # Slice Fruit using OPEN PALM
            # ==================================================

            if self.current_gesture == "OPEN PALM":

                if abs(self.hand_x - fruit["x"]) < 90 and abs(self.hand_y - fruit["y"]) < 90:

                    self.score += 1

                    self.combo += 1

                    if self.score > self.high_score:

                        self.high_score = self.score

                    self.effects.append({

                        "x": fruit["x"],

                        "y": fruit["y"],

                        "radius": 10,

                        "life": 12

                    })

                    self.sliced_fruits.append({

                        "x": fruit["x"],

                        "y": fruit["y"],

                        "vx": -3,

                        "vy": -4,

                        "gravity": 0.4,

                        "emoji": "◐"

                    })

                    self.sliced_fruits.append({

                        "x": fruit["x"],

                        "y": fruit["y"],

                        "vx": 3,

                        "vy": -4,

                        "gravity": 0.4,

                        "emoji": "◑"

                    })

                    remove.append(fruit)

                    continue

            # ==================================================
            # Remove fruit if it falls
            # (No Game Over - Endless Mode)
            # ==================================================

            if fruit["y"] > self.height() + 60:

                remove.append(fruit)

                self.combo = 0

        # ---------------- Remove Fruits ----------------

        for fruit in remove:

            if fruit in self.fruits:

                self.fruits.remove(fruit)

        # ---------------- Slice Animation ----------------

        dead = []

        for effect in self.effects:

            effect["radius"] += 5

            effect["life"] -= 1

            if effect["life"] <= 0:

                dead.append(effect)

        for effect in dead:

            self.effects.remove(effect)
        
        dead_parts = []

        for part in self.sliced_fruits:

            part["x"] += part["vx"]

            part["vy"] += part["gravity"]

            part["y"] += part["vy"]

            if part["y"] > self.height() + 50:

                dead_parts.append(part)

        for part in dead_parts:

            self.sliced_fruits.remove(part)

        self.update()
        # ==========================================================
    # Paint Game
    # ==========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        # ================= Background =================

        painter.fillRect(self.rect(), QColor(20, 20, 35))

        # ================= Score Panel =================

        painter.setPen(Qt.white)

        font = QFont()
        font.setPointSize(16)
        font.setBold(True)

        painter.setFont(font)

        painter.drawText(20, 35, f"Score : {self.score}")
        painter.drawText(20, 65, f"High Score : {self.high_score}")
        painter.drawText(20, 95, f"Combo : {self.combo}")

        # ================= Game Mode =================

        painter.setPen(QColor(0, 255, 255))

        font = QFont()
        font.setPointSize(13)

        painter.setFont(font)

        painter.drawText(
            self.width() - 250,
            35,
            "ENDLESS MODE"
        )

        painter.drawText(
            self.width() - 250,
            60,
            "✋ OPEN PALM = Slice"
        )

        # ================= Fruits =================

        fruit_font = QFont()
        fruit_font.setPointSize(30)

        painter.setFont(fruit_font)

        for fruit in self.fruits:

            painter.drawText(
                int(fruit["x"]),
                int(fruit["y"]),
                fruit["emoji"]
            )
        # ==========================================================
# Draw Sliced Fruit Parts
# ==========================================================

        slice_font = QFont()
        slice_font.setPointSize(30)
        painter.setFont(slice_font)

        for part in self.sliced_fruits:

            painter.drawText(
                int(part["x"]),
                int(part["y"]),
                part["emoji"]
        )
        # ================= Slice Effect =================

        painter.setPen(QColor(255, 255, 0))

        for effect in self.effects:

            painter.drawEllipse(

                int(effect["x"] - effect["radius"]),
                int(effect["y"] - effect["radius"]),

                effect["radius"] * 2,
                effect["radius"] * 2

            )

        # ================= Hand Pointer =================

        if self.current_gesture == "OPEN PALM":

            painter.setBrush(QColor(0, 255, 120))

        else:

            painter.setBrush(QColor(255, 80, 80))

        painter.setPen(Qt.NoPen)

        painter.drawEllipse(

            self.hand_x - 20,
            self.hand_y - 20,

            40,
            40

        )

        # ================= Gesture Name =================

        painter.setPen(Qt.white)

        font = QFont()
        font.setPointSize(12)

        painter.setFont(font)

        painter.drawText(

            self.hand_x + 25,
            self.hand_y,

            self.current_gesture

        )
        # ==========================================================
    # Window Resize
    # ==========================================================

    def resizeEvent(self, event):

        if self.hand_x > self.width():
            self.hand_x = self.width() // 2

        if self.hand_y > self.height():
            self.hand_y = self.height() // 2

        super().resizeEvent(event)

    # ==========================================================
    # Keyboard
    # ==========================================================

    def keyPressEvent(self, event):

        # ESC closes the game

        if event.key() == Qt.Key_Escape:

            self.close()

    # ==========================================================
    # Close Window
    # ==========================================================

    def closeEvent(self, event):

        if self.timer.isActive():

            self.timer.stop()

        event.accept()