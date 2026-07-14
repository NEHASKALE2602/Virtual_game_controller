import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import threading
import time

from detection.hand_detector import HandDetector
from detection.gesture_detector import GestureDetector
from controllers.game_controller import GameController
from utils.fps import FPS

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class VirtualGameController:

    def __init__(self):

        self.app = ctk.CTk()
        self.app.title("Virtual Game Controller")
        self.app.geometry("1400x850")
        self.app.resizable(False, False)

        self.camera = None
        self.running = False

        self.hand_detector = HandDetector()
        self.gesture_detector = GestureDetector()
        self.game_controller = GameController()
        self.fps = FPS()

        self.create_ui()

        def create_ui(self):

            title = ctk.CTkLabel(
                self.app,
                text="🎮 Virtual Game Controller",
                font=("Segoe UI",34,"bold")
            )
            title.pack(pady=(20,5))

            subtitle = ctk.CTkLabel(
                self.app,
                text="AI & ML Internship Project",
                font=("Segoe UI",18)
            )
            subtitle.pack()

            self.main = ctk.CTkFrame(
                self.app,
                corner_radius=20
            )

            self.main.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=20
            )

            self.left = ctk.CTkFrame(
                self.main,
                width=900,
                height=700,
                corner_radius=20
            )

            self.left.pack(
                side="left",
                padx=20,
                pady=20
            )

            self.right = ctk.CTkFrame(
                self.main,
                width=350,
                corner_radius=20
            )

            self.right.pack(
                side="right",
                fill="y",
                padx=20,
                pady=20
            )
            self.camera_label = ctk.CTkLabel(
                self.left,
                text=""
            )

            self.camera_label.pack(
                padx=15,
                pady=15
            )

            self.gesture = ctk.CTkLabel(
                self.right,
                text="Gesture : NONE",
                font=("Segoe UI",22,"bold")
            )
            self.gesture.pack(pady=20)

            self.action = ctk.CTkLabel(
                self.right,
                text="Action : NONE",
                font=("Segoe UI",22,"bold")
            )
            self.action.pack(pady=20)

            self.fps_label = ctk.CTkLabel(
                self.right,
                text="FPS : 0",
                font=("Segoe UI",22,"bold")
            )
            self.fps_label.pack(pady=20)

            self.status = ctk.CTkLabel(
                self.right,
                text="Status : Camera OFF",
                font=("Segoe UI",22,"bold"),
                text_color="red"
            )
            self.status.pack(pady=20)
            self.start_btn = ctk.CTkButton(
                self.right,
                text="▶ Start Camera",
                width=250,
                height=50,
                corner_radius=15,
                font=("Segoe UI",18,"bold"),
                command=self.start_camera
            )
            self.start_btn.pack(pady=(30,10))

            self.stop_btn = ctk.CTkButton(
                self.right,
                text="■ Stop Camera",
                width=250,
                height=50,
                corner_radius=15,
                fg_color="#C62828",
                hover_color="#8E0000",
                font=("Segoe UI",18,"bold"),
                command=self.stop_camera
            )
            self.stop_btn.pack(pady=10)

            self.clock = ctk.CTkLabel(
                self.right,
                text="",
                font=("Segoe UI",18)
            )
            self.clock.pack(pady=40)

            self.footer = ctk.CTkLabel(
                self.right,
                text="Developed by\nNeha Kale",
                font=("Segoe UI",18,"bold")
            )
            self.footer.pack(side="bottom", pady=20)

            self.update_clock()
        def update_clock(self):
            current = time.strftime("%d-%m-%Y\n%I:%M:%S %p")

            self.clock.configure(text=current)

            self.app.after(1000, self.update_clock)
        def start_camera(self):
            if self.running:
                return

            self.running = True

            self.status.configure(
                text="Status : Camera ON",
                text_color="green"
            )

            self.camera = cv2.VideoCapture(0)

            threading.Thread(
                target=self.update_camera,
                daemon=True
            ).start() 
        def stop_camera(self):

            self.running = False

            self.status.configure(
                text="Status : Camera OFF",
                text_color="red"
            )

            if self.camera:
                self.camera.release()
        def update_camera(self):

            while self.running:

                success, frame = self.camera.read()

                if not success:
                    continue

                frame = cv2.flip(frame, 1)

                frame, landmarks = self.hand_detector.detect(frame)

                gesture = "NONE"
                action = "Waiting..."

                if landmarks:

                    gesture = self.gesture_detector.recognize(landmarks)

                    self.game_controller.press_key(gesture)

                    action = gesture.replace("_", " ")

                fps = self.fps.calculate()

                self.gesture.configure(
                    text=f"Gesture : {gesture}"
                )

                self.action.configure(
                    text=f"Action : {action}"
                )

                self.fps_label.configure(
                    text=f"FPS : {fps}"
                )

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                image = Image.fromarray(frame)

                image = image.resize((860, 640))

                photo = ImageTk.PhotoImage(image=image)

                self.camera_label.configure(image=photo)

                self.camera_label.image = photo
                controller = VirtualGameController()
                controller.app.mainloop()
        

        