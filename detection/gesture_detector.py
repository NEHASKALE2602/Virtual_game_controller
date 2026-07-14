class GestureDetector:

    def fingers_up(self, landmarks):

        fingers = []

        # Thumb
        if landmarks[4][1] > landmarks[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Index
        if landmarks[8][2] < landmarks[6][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Middle
        if landmarks[12][2] < landmarks[10][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Ring
        if landmarks[16][2] < landmarks[14][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Pinky
        if landmarks[20][2] < landmarks[18][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        return fingers

    def recognize(self, landmarks):

        fingers = self.fingers_up(landmarks)

        print("Fingers:", fingers)

    # ☝️ One Finger (Run Car)
        if fingers == [0, 1, 0, 0, 0]:
            return "ACCELERATE"

    # ✌️ Two Fingers (Turn Left)
        elif fingers == [0, 1, 1, 0, 0]:
            return "LEFT"

    # 🤟 Three Fingers (Turn Right)
        elif fingers == [0, 1, 1, 1, 0]:
            return "RIGHT"

    # 🖐️ Open Palm (Stop Car)
        elif fingers == [1, 1, 1, 1, 1] or fingers == [0, 1, 1, 1, 1]:
            return "BRAKE"

        else:
            return "NONE"