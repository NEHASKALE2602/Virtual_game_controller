class GestureDetector:

    def recognize(self, landmarks):

        if len(landmarks) == 0:
            return "NO HAND"

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

        # -----------------------------
        # Static Gestures
        # -----------------------------

        if fingers == [1, 1, 1, 1, 1]:
            return "OPEN PALM"

        if fingers == [0, 0, 0, 0, 0]:
            return "FIST"

        if fingers == [0, 1, 0, 0, 0]:
            return "POINTING"

        if fingers == [0, 1, 1, 0, 0]:
            return "PEACE"

        if fingers == [1, 0, 0, 0, 0]:
            return "THUMB UP"

        # -----------------------------
        # Direction Gestures
        # -----------------------------

        wrist_x = landmarks[0][1]
        wrist_y = landmarks[0][2]

        index_x = landmarks[8][1]
        index_y = landmarks[8][2]

        dx = index_x - wrist_x
        dy = index_y - wrist_y

        if abs(dx) > abs(dy):

            if dx > 120:
                return "RIGHT"

            elif dx < -120:
                return "LEFT"

        else:

            if dy < -120:
                return "UP"

            elif dy > 120:
                return "DOWN"

        return "UNKNOWN"