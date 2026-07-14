import pyautogui
import time

pyautogui.FAILSAFE = False


class GameController:

    def __init__(self):

        self.last_time = time.time()
        self.cooldown = 0.20

    def press_key(self, gesture):

        current_time = time.time()

        if current_time - self.last_time < self.cooldown:
            return

        if gesture == "ACCELERATE":

            pyautogui.keyDown("up")
            pyautogui.keyUp("down")
            print("RUN")

        elif gesture == "LEFT":

            pyautogui.press("left")
            print("LEFT")

        elif gesture == "RIGHT":

            pyautogui.press("right")
            print("RIGHT")

        elif gesture == "BRAKE":

            pyautogui.keyUp("up")
            pyautogui.keyDown("down")
            print("STOP")

        else:

            pyautogui.keyUp("up")
            pyautogui.keyUp("down")

        self.last_time = current_time