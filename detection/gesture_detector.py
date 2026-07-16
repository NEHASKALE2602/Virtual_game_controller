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

        if len(landmarks) < 21:
            return "NONE"

        fingers = self.fingers_up(landmarks)

        if fingers == [0, 1, 0, 0, 0]:
            return "ACCELERATE"

        elif fingers == [0, 1, 1, 0, 0]:
            return "LEFT"

        elif fingers == [0, 1, 1, 1, 0]:
            return "RIGHT"

        elif fingers == [1, 1, 1, 1, 1] or fingers == [0, 1, 1, 1, 1]:
            return "BRAKE"

            return "NONE"