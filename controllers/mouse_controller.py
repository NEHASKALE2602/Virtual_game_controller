import pyautogui
from utils.gesture_utils import calculate_distance

pyautogui.FAILSAFE = False


class MouseController:

    def __init__(self):

        # Screen Size
        self.screen_width, self.screen_height = pyautogui.size()

        # Previous Mouse Position
        self.prev_x = 0
        self.prev_y = 0

        # Smooth Mouse Movement
        self.smoothening = 7

        # Gesture States
        self.left_clicked = False
        self.right_clicked = False
        self.scrolled = False
        self.dragging = False

        # Distance Thresholds
        self.left_threshold = 35
        self.right_threshold = 35
        self.scroll_threshold = 35
        self.drag_threshold = 35

    # ==========================================
    # Mouse Movement
    # ==========================================
    def move(self, x, y, frame_width, frame_height):

        screen_x = (x / frame_width) * self.screen_width
        screen_y = (y / frame_height) * self.screen_height

        curr_x = self.prev_x + (screen_x - self.prev_x) / self.smoothening
        curr_y = self.prev_y + (screen_y - self.prev_y) / self.smoothening

        pyautogui.moveTo(curr_x, curr_y)

        self.prev_x = curr_x
        self.prev_y = curr_y

    # ==========================================
    # Left Click
    # Thumb + Index
    # ==========================================
    def left_click(self, landmarks):

        distance = calculate_distance(landmarks[4], landmarks[8])

        if distance < self.left_threshold:

            if not self.left_clicked:

                pyautogui.click(button="left")
                print("LEFT CLICK")

                self.left_clicked = True

        else:

            self.left_clicked = False

    # ==========================================
    # Right Click
    # Thumb + Middle
    # ==========================================
    def right_click(self, landmarks):

        distance = calculate_distance(landmarks[4], landmarks[12])

        if distance < self.right_threshold:

            if not self.right_clicked:

                pyautogui.click(button="right")
                print("RIGHT CLICK")

                self.right_clicked = True

        else:

            self.right_clicked = False

    # ==========================================
    # Scroll Up
    # Thumb + Ring
    # ==========================================
    def scroll(self, landmarks):

        distance = calculate_distance(landmarks[4], landmarks[16])

        if distance < self.scroll_threshold:

            if not self.scrolled:

                pyautogui.scroll(400)
                print("SCROLL UP")

                self.scrolled = True

        else:

            self.scrolled = False

    # ==========================================
    # Drag & Drop
    # Thumb + Pinky
    # ==========================================
    def drag_drop(self, landmarks):

        distance = calculate_distance(landmarks[4], landmarks[20])

        if distance < self.drag_threshold:

            if not self.dragging:

                pyautogui.mouseDown()

                print("DRAG START")

                self.dragging = True

        else:

            if self.dragging:

                pyautogui.mouseUp()

                print("DROP")

                self.dragging = False