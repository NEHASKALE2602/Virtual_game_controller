import random

from PySide6.QtCore import Qt, QTimer, QRectF, QPointF
from PySide6.QtGui import (
    QPainter,
    QColor,
    QBrush,
    QPen,
    QFont
)
from PySide6.QtWidgets import QWidget, QPushButton

from controller.controller_manager import controller


class FlappyGame(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Flappy Bird")

        self.resize(1000, 650)

        self.setMinimumSize(1000, 650)

        self.setFocusPolicy(Qt.StrongFocus)

        self.timer = QTimer()

        self.timer.timeout.connect(self.update_game)

        self.timer.start(16)

        self.reset_game()
            # ==========================================================
    # RESET GAME
    # ==========================================================

    def reset_game(self):

        # -----------------------------
        # Bird
        # -----------------------------

        self.bird_x = 220
        self.bird_y = 300

        self.bird_radius = 22

        self.velocity = -8

        self.gravity = 0.8

        self.jump_force = -12

        self.rotation = 0

        self.wing_angle = 0

        self.wing_direction = 1

        # -----------------------------
        # Gesture
        # -----------------------------

        self.previous_gesture = "NO HAND"

        # -----------------------------
        # Background
        # -----------------------------

        self.background_offset = 0

        self.ground_offset = 0

        self.clouds = []

        for i in range(6):

            self.clouds.append({

                "x": random.randint(0, 1000),

                "y": random.randint(40, 220),

                "speed": random.uniform(0.5, 1.5)

            })

        # -----------------------------
        # Pipes
        # -----------------------------

        self.pipe_width = 100

        self.pipe_gap = 220

        self.pipe_speed = 5

        self.pipes = []

        start_x = 900

        for i in range(3):

            top = random.randint(120, 320)

            self.pipes.append({

                "x": start_x + i * 350,

                "top": top,

                "passed": False

            })

        # -----------------------------
        # Game
        # -----------------------------

        self.score = 0

        self.high_score = 0

        self.missed = 0

        self.max_missed = 3

        self.game_over = False
            # ==========================================================
    # UPDATE GAME
    # ==========================================================

    def update_game(self):

        if self.game_over:
            self.update()
            return

        # ------------------------------------------------------
        # Gesture Control (Jump only once)
        # ------------------------------------------------------

        gesture = controller.get_gesture()
        print(gesture)

        if gesture != "NO HAND" and gesture != self.previous_gesture:
            self.velocity = self.jump_force
            
        self.previous_gesture = gesture

        # ------------------------------------------------------
        # Bird Physics
        # ------------------------------------------------------

        self.velocity += self.gravity

        if self.velocity > 12:
            self.velocity = 12

        self.bird_y += self.velocity

        # Bird Rotation

        if self.velocity < 0:

            self.rotation = -25

        else:

            self.rotation = min(45, self.rotation + 2)

        # ------------------------------------------------------
        # Wing Animation
        # ------------------------------------------------------

        self.wing_angle += self.wing_direction * 4

        if self.wing_angle > 25:

            self.wing_direction = -1

        elif self.wing_angle < -25:

            self.wing_direction = 1

        # ------------------------------------------------------
        # Background Animation
        # ------------------------------------------------------

        self.background_offset -= 1

        self.ground_offset -= self.pipe_speed

        if self.ground_offset <= -40:

            self.ground_offset = 0

        # ------------------------------------------------------
        # Clouds
        # ------------------------------------------------------

        for cloud in self.clouds:

            cloud["x"] -= cloud["speed"]

            if cloud["x"] < -120:

                cloud["x"] = self.width() + random.randint(50, 250)

                cloud["y"] = random.randint(40, 220)

        # ------------------------------------------------------
        # Ground Collision
        # ------------------------------------------------------

        ground = self.height() - 80

        if self.bird_y + self.bird_radius >= ground:

            self.game_over = True

        if self.bird_y < 0:

            self.bird_y = 0

            self.velocity = 0

        self.update()
            # ==========================================================
    # UPDATE PIPES
    # ==========================================================

        for pipe in self.pipes:

            # Move Pipe

            pipe["x"] -= self.pipe_speed

            # --------------------------------------------------
            # Recycle Pipe
            # --------------------------------------------------

            if pipe["x"] + self.pipe_width < 0:

                pipe["x"] = max(p["x"] for p in self.pipes) + 350

                pipe["top"] = random.randint(120, 320)

                pipe["passed"] = False

                self.missed += 1

                if self.missed >= self.max_missed:

                    self.game_over = True

            # --------------------------------------------------
            # Score
            # --------------------------------------------------

            if (not pipe["passed"]) and (pipe["x"] + self.pipe_width < self.bird_x):

                pipe["passed"] = True

                self.score += 1

                if self.score > self.high_score:

                    self.high_score = self.score

            # --------------------------------------------------
            # Collision
            # --------------------------------------------------

            bird_left = self.bird_x - self.bird_radius
            bird_right = self.bird_x + self.bird_radius

            bird_top = self.bird_y - self.bird_radius
            bird_bottom = self.bird_y + self.bird_radius

            pipe_left = pipe["x"]
            pipe_right = pipe["x"] + self.pipe_width

            if bird_right > pipe_left and bird_left < pipe_right:

                if bird_top < pipe["top"] or \
                   bird_bottom > pipe["top"] + self.pipe_gap:

                    self.game_over = True

        self.update()
    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

    # ======================================================
    # SKY
    # ======================================================

        painter.fillRect(self.rect(), QColor(110, 200, 255))

    # ======================================================
    # CLOUDS
    # ======================================================

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255, 210))

        for cloud in self.clouds:

            x = cloud["x"]
            y = cloud["y"]

            painter.drawEllipse(int(x), int(y), 70, 40)
            painter.drawEllipse(int(x + 30), int(y - 15), 70, 50)
            painter.drawEllipse(int(x + 60), int(y), 70, 40)

    # ======================================================
    # PIPES
    # ======================================================

        painter.setBrush(QColor(40, 180, 40))

        for pipe in self.pipes:

        # Top Pipe
            painter.drawRoundedRect(
                pipe["x"],
                0,
                self.pipe_width,
                pipe["top"],
                8,
                8
            )

        # Bottom Pipe
            bottom = pipe["top"] + self.pipe_gap

            painter.drawRoundedRect(
                pipe["x"],
                bottom,
                self.pipe_width,
                self.height() - bottom - 80,
                8,
                8
            )

    # ======================================================
    # GROUND
    # ======================================================

        ground_y = self.height() - 80

        painter.setBrush(QColor(210, 180, 90))

        painter.drawRect(
            0,
            ground_y,
            self.width(),
            80
        )

        painter.setPen(QPen(QColor(170, 140, 60), 2))

        x = int(self.ground_offset)

        while x < self.width():

            painter.drawLine(
                x,
                ground_y,
                x + 40,
                ground_y + 80
            )

            x += 40

    # ======================================================
    # BIRD
    # ======================================================

        painter.save()

        painter.translate(self.bird_x, self.bird_y)

        painter.rotate(self.rotation)

        painter.setPen(Qt.NoPen)

    # Body

        painter.setBrush(QColor(255, 220, 0))

        painter.drawEllipse(
            -20,
            -20,
            40,
            40
        )

    # Wing

        painter.save()

        painter.rotate(self.wing_angle)

        painter.setBrush(QColor(255, 180, 0))

        painter.drawEllipse(
            -10,
            -5,
            24,
            14
        )

        painter.restore()

    # Eye

        painter.setBrush(Qt.white)

        painter.drawEllipse(5, -10, 10, 10)

        painter.setBrush(Qt.black)

        painter.drawEllipse(9, -6, 4, 4)

    # Beak

        painter.setBrush(QColor(255, 120, 0))

        painter.drawPolygon([
                QPointF(20, 0),
                QPointF(32, -4),
                QPointF(20, 6)
        ])

        painter.restore()

    # ======================================================
    # SCORE
    # ======================================================

        painter.setPen(Qt.white)

        font = QFont("Segoe UI", 18, QFont.Bold)

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

        painter.drawText(
            20,
            95,
            f"Missed : {self.missed}/{self.max_missed}"
        )

    # ======================================================
    # GAME OVER
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

        # ------------------------------------
        # Restart Game
        # ------------------------------------

        if event.key() == Qt.Key_R and self.game_over:

            self.reset_game()

            return

        # ------------------------------------
        # Exit Game
        # ------------------------------------

        if event.key() == Qt.Key_Escape:

            self.close()

            return

    # ==========================================================
    # WINDOW EVENTS
    # ==========================================================

    def showEvent(self, event):

        self.timer.start(16)

        super().showEvent(event)

    def hideEvent(self, event):

        self.timer.stop()

        super().hideEvent(event)

    def closeEvent(self, event):

        if self.timer.isActive():

            self.timer.stop()

        event.accept()