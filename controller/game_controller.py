class GameController:

    def __init__(self):

        self.current_gesture = "NONE"
        self.hand_position = (0, 0)

    def set_gesture(self, gesture):

        self.current_gesture = gesture

    def get_gesture(self):

        return self.current_gesture

    def set_hand_position(self, x, y):

        self.hand_position = (x, y)

    def get_hand_position(self):

        return self.hand_position