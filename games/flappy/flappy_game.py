import random

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget

from controller.controller_manager import controller


class FlappyGame(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(900, 600)
        self.setFocusPolicy(Qt.StrongFocus)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(30)

        self.reset_game()

    def reset_game(self):

        # Bird
        self.bird_x = 180
        self.bird_y = 250

        self.velocity = 0
        self.gravity = 1
        self.jump_force = -12

        # Score
        self.score = 0

        # Pipe
        self.pipe_x = 700
        self.pipe_width = 80
        self.pipe_gap = 180
        self.pipe_top = random.randint(100, 300)
        self.pipe_speed = 6

        self.pipe_passed = False

    def update_game(self):

        # ---------------- Gesture Control ----------------

        gesture = controller.get_gesture()

        if gesture == "Open Palm":
            self.velocity = self.jump_force

        # ---------------- Gravity ----------------

        self.velocity += self.gravity
        self.bird_y += self.velocity

        # Top Boundary

        if self.bird_y < 0:
            self.bird_y = 0
            self.velocity = 0

        # Bottom Boundary

        if self.bird_y > self.height() - 40:
            self.reset_game()
            return

        # ---------------- Pipe Movement ----------------

        self.pipe_x -= self.pipe_speed

        if self.pipe_x < -self.pipe_width:

            self.pipe_x = self.width()
            self.pipe_top = random.randint(100, 300)
            self.pipe_passed = False

        # ---------------- Score ----------------

        if (not self.pipe_passed) and (self.pipe_x + self.pipe_width < self.bird_x):

            self.score += 1
            self.pipe_passed = True

        # ---------------- Collision ----------------

        bird_left = self.bird_x
        bird_right = self.bird_x + 40
        bird_top = self.bird_y
        bird_bottom = self.bird_y + 40

        pipe_left = self.pipe_x
        pipe_right = self.pipe_x + self.pipe_width

        if bird_right > pipe_left and bird_left < pipe_right:

            if bird_top < self.pipe_top or bird_bottom > self.pipe_top + self.pipe_gap:

                self.reset_game()
                return

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        # Background

        painter.fillRect(self.rect(), QColor(90, 180, 255))

        # ---------------- Top Pipe ----------------

        painter.setBrush(QColor(0, 170, 0))
        painter.setPen(Qt.NoPen)

        painter.drawRect(
            self.pipe_x,
            0,
            self.pipe_width,
            self.pipe_top
        )

        # ---------------- Bottom Pipe ----------------

        bottom_y = self.pipe_top + self.pipe_gap

        painter.drawRect(
            self.pipe_x,
            bottom_y,
            self.pipe_width,
            self.height() - bottom_y
        )

        # ---------------- Bird ----------------

        painter.setBrush(QColor(255, 220, 0))

        painter.drawEllipse(
            self.bird_x,
            self.bird_y,
            40,
            40
        )

        # Eye

        painter.setBrush(Qt.black)

        painter.drawEllipse(
            self.bird_x + 24,
            self.bird_y + 10,
            6,
            6
        )

        # Beak

        painter.setBrush(QColor(255, 120, 0))

        painter.drawRect(
            self.bird_x + 38,
            self.bird_y + 18,
            10,
            6
        )

        # ---------------- Score ----------------

        painter.setPen(Qt.white)

        painter.drawText(
            20,
            30,
            f"Score : {self.score}"
        )

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Space:

            self.velocity = self.jump_force