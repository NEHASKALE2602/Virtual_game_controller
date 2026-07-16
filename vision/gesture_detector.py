class GestureDetector:

    def recognize(self, landmarks):

        if len(landmarks) == 0:
            return "NO HAND"

        # -----------------------------
        # Finger Tips
        # -----------------------------

        tips = [4, 8, 12, 16, 20]

        fingers = []

        # Thumb

        if landmarks[4][1] > landmarks[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other Fingers

        for tip in tips[1:]:

            if landmarks[tip][2] < landmarks[tip - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # -----------------------------
        # Hand Center
        # -----------------------------

        wrist_x = landmarks[0][1]
        wrist_y = landmarks[0][2]

        index_x = landmarks[8][1]
        index_y = landmarks[8][2]

        dx = index_x - wrist_x
        dy = index_y - wrist_y

        # -----------------------------
        # Direction Detection
        # -----------------------------

        if abs(dx) > abs(dy):

            if dx > 80:
                return "RIGHT"

            elif dx < -80:
                return "LEFT"

        else:

            if dy < -80:
                return "UP"

            elif dy > 80:
                return "DOWN"

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

        if fingers == [1, 1, 0, 0, 1]:
            return "OK"

        return "UNKNOWN"