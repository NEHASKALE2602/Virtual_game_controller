from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame
)


class InfoCard(QFrame):

    def __init__(self, title, value):

        super().__init__()

        self.setObjectName("infoCard")

        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 20, 20, 20)

        self.title = QLabel(title)
        self.title.setObjectName("infoTitle")

        self.value = QLabel(value)
        self.value.setObjectName("infoValue")
        self.value.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.value)


class GesturePage(QWidget):

    def __init__(self):

        super().__init__()

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(30, 30, 30, 30)

        main_layout.setSpacing(25)

        # =====================================
        # Title
        # =====================================

        title = QLabel("🤖 AI Gesture Recognition")

        title.setObjectName("pageTitle")

        title.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title)

        # =====================================
        # Current Gesture
        # =====================================

        self.gesture_icon = QLabel("✋")

        self.gesture_icon.setAlignment(Qt.AlignCenter)

        self.gesture_icon.setObjectName("gestureIcon")

        self.gesture_name = QLabel("OPEN PALM")

        self.gesture_name.setAlignment(Qt.AlignCenter)

        self.gesture_name.setObjectName("gestureName")

        main_layout.addWidget(self.gesture_icon)

        main_layout.addWidget(self.gesture_name)

        # =====================================
        # Information Cards
        # =====================================

        grid = QGridLayout()

        grid.setHorizontalSpacing(20)

        grid.setVerticalSpacing(20)

        self.ai_card = InfoCard("AI Status", "ACTIVE")

        self.track_card = InfoCard("Tracking", "TRACKING")

        self.conf_card = InfoCard("Confidence", "100%")

        self.hand_card = InfoCard("Hands", "1")

        self.finger_card = InfoCard("Fingers", "5")

        self.fps_card = InfoCard("FPS", "30")

        grid.addWidget(self.ai_card, 0, 0)

        grid.addWidget(self.track_card, 0, 1)

        grid.addWidget(self.conf_card, 0, 2)

        grid.addWidget(self.hand_card, 1, 0)

        grid.addWidget(self.finger_card, 1, 1)

        grid.addWidget(self.fps_card, 1, 2)

        main_layout.addLayout(grid)
                # =====================================
        # Supported Gestures
        # =====================================

        supported_title = QLabel("Supported Gestures")

        supported_title.setObjectName("sectionTitle")

        supported_title.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(supported_title)

        gesture_grid = QGridLayout()

        gesture_grid.setHorizontalSpacing(15)

        gesture_grid.setVerticalSpacing(15)

        gestures = [

            ("✋", "Open Palm"),
            ("☝", "Pointing"),
            ("✊", "Fist"),

            ("✌", "Peace"),
            ("👍", "Thumb Up"),
            ("⬅", "Left"),

            ("➡", "Right"),
            ("⬆", "Up"),
            ("⬇", "Down")

        ]

        row = 0
        col = 0

        for icon, name in gestures:

            card = QFrame()

            card.setObjectName("gestureCard")

            layout = QVBoxLayout(card)

            layout.setContentsMargins(15, 15, 15, 15)

            emoji = QLabel(icon)

            emoji.setAlignment(Qt.AlignCenter)

            emoji.setObjectName("gestureEmoji")

            text = QLabel(name)

            text.setAlignment(Qt.AlignCenter)

            text.setObjectName("gestureText")

            layout.addWidget(emoji)

            layout.addWidget(text)

            gesture_grid.addWidget(card, row, col)

            col += 1

            if col == 3:

                col = 0

                row += 1

        main_layout.addLayout(gesture_grid)

        # =====================================
        # AI Status
        # =====================================

        self.engine_status = QLabel("🟢 AI Gesture Recognition Running")

        self.engine_status.setObjectName("engineStatus")

        self.engine_status.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(self.engine_status)

        main_layout.addStretch()
            # =====================================================
    # Update Methods
    # =====================================================

    def set_gesture(
        self,
        name="OPEN PALM",
        icon="✋",
        confidence=100,
        fingers=5,
        hands=1,
        tracking=True,
        fps=30,
    ):
        """
        Update the gesture information.
        """

        self.gesture_name.setText(name.upper())
        self.gesture_icon.setText(icon)

        self.conf_card.value.setText(f"{confidence}%")
        self.hand_card.value.setText(str(hands))
        self.finger_card.value.setText(str(fingers))
        self.fps_card.value.setText(str(fps))

        if tracking:
            self.track_card.value.setText("TRACKING")
        else:
            self.track_card.value.setText("LOST")

    def set_ai_status(self, active=True):
        """
        Update AI Engine status.
        """

        if active:
            self.ai_card.value.setText("ACTIVE")
            self.engine_status.setText("🟢 AI Gesture Recognition Running")
        else:
            self.ai_card.value.setText("STOPPED")
            self.engine_status.setText("🔴 AI Gesture Recognition Stopped")

    def update_fps(self, fps):
        self.fps_card.value.setText(str(fps))

    def update_confidence(self, confidence):
        self.conf_card.value.setText(f"{confidence}%")

    def update_tracking(self, tracking):
        if tracking:
            self.track_card.value.setText("TRACKING")
        else:
            self.track_card.value.setText("LOST")

    def update_hands(self, count):
        self.hand_card.value.setText(str(count))

    def update_fingers(self, count):
        self.finger_card.value.setText(str(count))

    def reset(self):
        """
        Reset UI to default state.
        """

        self.gesture_icon.setText("✋")
        self.gesture_name.setText("NO GESTURE")

        self.ai_card.value.setText("ACTIVE")
        self.track_card.value.setText("WAITING")
        self.conf_card.value.setText("0%")
        self.hand_card.value.setText("0")
        self.finger_card.value.setText("0")
        self.fps_card.value.setText("0")

        self.engine_status.setText("🟡 Waiting for Hand...")