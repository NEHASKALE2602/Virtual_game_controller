import cv2
import time

from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

from vision.hand_detector import HandDetector
from vision.gesture_detector import GestureDetector

from controller.controller_manager import controller


class CameraThread(QThread):

    frame_received = Signal(QImage)
    camera_data = Signal(dict)

    def __init__(self):
        super().__init__()

        self.running = True

        self.hand_detector = HandDetector()
        self.gesture_detector = GestureDetector()

        self.previous_time = time.time()

    def run(self):

        cap = cv2.VideoCapture(0)

        while self.running:

            ret, frame = cap.read()

            if not ret:
                continue

            # Flip Camera
            frame = cv2.flip(frame, 1)

            # Hand Detection
            frame, landmarks = self.hand_detector.detect(frame)
            if self.hand_detector.hand_center:

                x, y = self.hand_detector.hand_center

                controller.set_hand_position(x, y)

            # FPS
            current_time = time.time()

            fps = int(1 / (current_time - self.previous_time))

            self.previous_time = current_time

            # Gesture Detection
            gesture = self.gesture_detector.recognize(landmarks)

            # Send Gesture to Controller
            controller.set_gesture(gesture)

            # Draw FPS
            cv2.putText(
                frame,
                f"FPS : {fps}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # Draw Gesture
            cv2.putText(
                frame,
                f"Gesture : {gesture}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                2
            )

            # Info Panel Data
            hands = 1 if landmarks else 0
            confidence = 100 if landmarks else 0

            data = {
                "camera": "Connected",
                "ai": "Active",
                "gesture": gesture,
                "confidence": f"{confidence}%",
                "fps": str(fps),
                "hands": str(hands)
            }

            self.camera_data.emit(data)

            # Convert Frame for Qt
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            h, w, ch = rgb.shape

            image = QImage(
                rgb.data,
                w,
                h,
                ch * w,
                QImage.Format_RGB888
            )

            self.frame_received.emit(image)

        cap.release()

    def stop(self):

        self.running = False
        self.wait()