import keyboard
import time


class KeyboardController:

    def __init__(self):

        self.last_action = 0
        self.delay = 0.5

    def press_key(self, gesture):

        current_time = time.time()

        if current_time - self.last_action < self.delay:
            return

        if gesture == "FIST":

            keyboard.press_and_release("space")
            print("SPACE")

        elif gesture == "THUMB":

            keyboard.press_and_release("enter")
            print("ENTER")

        elif gesture == "VICTORY":

            keyboard.press_and_release("right")
            print("RIGHT ARROW")

        elif gesture == "INDEX":

            keyboard.press_and_release("left")
            print("LEFT ARROW")

        self.last_action = current_time