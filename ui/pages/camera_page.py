from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QPushButton
)
from PySide6.QtGui import QPixmap

from vision.camera_thread import CameraThread


class CameraPage(QWidget):

    def __init__(self):
        super().__init__()

        # =========================
        # Main Layout
        # =========================

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # =========================
        # Left Panel
        # =========================

        left = QFrame()
        left.setObjectName("cameraFrame")

        left_layout = QVBoxLayout(left)

        title = QLabel("📷 Live Camera")
        title.setObjectName("pageTitle")

        # Camera Buttons

        button_layout = QHBoxLayout()

        self.start_button = QPushButton("▶ Start Camera")
        self.start_button.setObjectName("cameraButton")

        self.stop_button = QPushButton("⏹ Stop Camera")
        self.stop_button.setObjectName("cameraButton")
        self.stop_button.setEnabled(False)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addStretch()

        # Camera Preview

        self.camera_label = QLabel("Camera Stopped")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setMinimumSize(800, 550)
        self.camera_label.setObjectName("cameraLabel")

        left_layout.addWidget(title)
        left_layout.addLayout(button_layout)
        left_layout.addWidget(self.camera_label)

        # =========================
        # Right Panel
        # =========================

        right = QFrame()
        right.setObjectName("infoPanel")
        right.setFixedWidth(300)

        right_layout = QVBoxLayout(right)

        self.info_labels = {}

        info = [

            ("Camera", "Disconnected"),
            ("AI Status", "Stopped"),
            ("Gesture", "None"),
            ("Confidence", "0%"),
            ("FPS", "0"),
            ("Hands", "0")

        ]

        for title_text, value_text in info:

            card = QFrame()
            card.setObjectName("infoCard")

            layout = QVBoxLayout(card)

            title_label = QLabel(title_text)
            title_label.setObjectName("infoTitle")

            value_label = QLabel(value_text)
            value_label.setObjectName("infoValue")

            self.info_labels[title_text] = value_label

            layout.addWidget(title_label)
            layout.addWidget(value_label)

            right_layout.addWidget(card)

        right_layout.addStretch()

        # =========================
        # Add Panels
        # =========================

        main_layout.addWidget(left, 4)
        main_layout.addWidget(right, 1)

        # =========================
        # Camera Thread
        # =========================

        self.camera_thread = None

        self.start_button.clicked.connect(self.start_camera)
        self.stop_button.clicked.connect(self.stop_camera)

    # ==========================================
    # Start Camera
    # ==========================================

    def start_camera(self):

        if self.camera_thread is None:

            self.camera_thread = CameraThread()

            self.camera_thread.frame_received.connect(self.update_frame)
            self.camera_thread.camera_data.connect(self.update_camera_info)

            self.camera_thread.start()

            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

    # ==========================================
    # Stop Camera
    # ==========================================

    def stop_camera(self):

        if self.camera_thread:

            self.camera_thread.stop()
            self.camera_thread = None

            self.camera_label.clear()
            self.camera_label.setText("Camera Stopped")

            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

            self.info_labels["Camera"].setText("Disconnected")
            self.info_labels["AI Status"].setText("Stopped")
            self.info_labels["Gesture"].setText("None")
            self.info_labels["Confidence"].setText("0%")
            self.info_labels["FPS"].setText("0")
            self.info_labels["Hands"].setText("0")

    # ==========================================
    # Update Camera Frame
    # ==========================================

    def update_frame(self, image):

        pixmap = QPixmap.fromImage(image)

        self.camera_label.setPixmap(

            pixmap.scaled(

                self.camera_label.size(),

                Qt.KeepAspectRatio,

                Qt.SmoothTransformation

            )

        )

    # ==========================================
    # Update Right Side Information
    # ==========================================

    def update_camera_info(self, data):

        self.info_labels["Camera"].setText(data["camera"])
        self.info_labels["AI Status"].setText(data["ai"])
        self.info_labels["Gesture"].setText(data["gesture"])
        self.info_labels["Confidence"].setText(data["confidence"])
        self.info_labels["FPS"].setText(data["fps"])
        self.info_labels["Hands"].setText(data["hands"])

        if hasattr(self, "dashboard"):

            self.dashboard.update_card(
                "📷 Camera Status",
                data["camera"]
            )

            self.dashboard.update_card(
                "🤖 AI Status",
                data["ai"]
            )

            self.dashboard.update_card(
                "✋ Current Gesture",
                data["gesture"]
            )

            self.dashboard.update_card(
                "🙌 Hands Detected",
                data["hands"]
            )

            self.dashboard.update_card(
                "⚡ FPS",
                data["fps"]
            )

    # ==========================================
    # Close Event
    # ==========================================

    def closeEvent(self, event):

        if self.camera_thread:

            self.camera_thread.stop()

        event.accept()