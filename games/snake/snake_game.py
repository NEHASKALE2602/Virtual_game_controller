import random

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget

from controller.controller_manager import controller


class SnakeGame(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(900, 600)
        self.setFocusPolicy(Qt.StrongFocus)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(120)

        self.high_score = 0

        self.reset_game()

    def reset_game(self):

        self.snake = [
            (10, 10),
            (9, 10),
            (8, 10)
        ]

        self.direction = "RIGHT"
        self.score = 0
        self.food = self.generate_food()

        self.update()

    def generate_food(self):

        while True:

            food = (
                random.randint(0, 29),
                random.randint(0, 19)
            )

            if food not in self.snake:
                return food

    def update_game(self):

        # -----------------------------
        # Hand Position Control
        # -----------------------------

        x, y = controller.get_hand_position()

        if x != 0:

            if x < 250:
                self.direction = "LEFT"

            elif x > 450:
                self.direction = "RIGHT"

        if y != 0:

            if y < 180:
                self.direction = "UP"

            elif y > 320:
                self.direction = "DOWN"

        # -----------------------------
        # Gesture Control
        # -----------------------------

        gesture = controller.get_gesture()

        if gesture == "LEFT":
            self.direction = "LEFT"

        elif gesture == "RIGHT":
            self.direction = "RIGHT"

        elif gesture == "UP":
            self.direction = "UP"

        elif gesture == "DOWN":
            self.direction = "DOWN"

        # -----------------------------
        # Move Snake
        # -----------------------------

        head_x, head_y = self.snake[0]

        if self.direction == "RIGHT":
            head_x += 1

        elif self.direction == "LEFT":
            head_x -= 1

        elif self.direction == "UP":
            head_y -= 1

        elif self.direction == "DOWN":
            head_y += 1

        # -----------------------------
        # Screen Wrapping
        # -----------------------------

        if head_x < 0:
            head_x = 29

        elif head_x > 29:
            head_x = 0

        if head_y < 0:
            head_y = 19

        elif head_y > 19:
            head_y = 0

        new_head = (head_x, head_y)

        self.snake.insert(0, new_head)

        # -----------------------------
        # Food Collision
        # -----------------------------

        if new_head == self.food:

            self.score += 10

            if self.score > self.high_score:
                self.high_score = self.score

            self.food = self.generate_food()

        else:

            self.snake.pop()

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        # Background
        painter.fillRect(self.rect(), QColor(18, 18, 30))

        cell = 25

        # ---------------- Grid ----------------

        painter.setPen(QColor(35, 35, 45))

        for x in range(0, self.width(), cell):
            painter.drawLine(x, 0, x, self.height())

        for y in range(0, self.height(), cell):
            painter.drawLine(0, y, self.width(), y)

        # ---------------- Score ----------------

        painter.setPen(Qt.white)

        painter.drawText(
            20,
            30,
            f"Score : {self.score}"
        )

        painter.drawText(
            170,
            30,
            f"High Score : {self.high_score}"
        )

        # ---------------- Snake ----------------

        painter.setPen(Qt.NoPen)

        for i, (x, y) in enumerate(self.snake):

            if i == 0:
                painter.setBrush(QColor(0, 255, 120))
            else:
                painter.setBrush(QColor(0, 190, 90))

            painter.drawRoundedRect(
                x * cell + 2,
                y * cell + 2,
                cell - 4,
                cell - 4,
                8,
                8
            )

        # ---------------- Food ----------------

        painter.setBrush(QColor(255, 70, 70))

        painter.drawEllipse(
            self.food[0] * cell + 3,
            self.food[1] * cell + 3,
            cell - 6,
            cell - 6
        )

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Left:
            self.direction = "LEFT"

        elif event.key() == Qt.Key_Right:
            self.direction = "RIGHT"

        elif event.key() == Qt.Key_Up:
            self.direction = "UP"

        elif event.key() == Qt.Key_Down:
            self.direction = "DOWN"