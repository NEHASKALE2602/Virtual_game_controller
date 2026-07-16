import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.drawer = mp.solutions.drawing_utils

        # Hand Center
        self.hand_center = None

        # Index Finger Tip
        self.index_tip = None

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        landmarks = []

        self.hand_center = None
        self.index_tip = None

        if results.multi_hand_landmarks:

            hand = results.multi_hand_landmarks[0]

            self.drawer.draw_landmarks(
                frame,
                hand,
                self.mp_hands.HAND_CONNECTIONS
            )

            h, w, _ = frame.shape

            for idx, lm in enumerate(hand.landmark):

                x = int(lm.x * w)
                y = int(lm.y * h)

                landmarks.append([idx, x, y])

            # -----------------------------
            # Hand Center
            # -----------------------------

            wrist = landmarks[0]
            middle = landmarks[9]

            cx = (wrist[1] + middle[1]) // 2
            cy = (wrist[2] + middle[2]) // 2

            self.hand_center = (cx, cy)

            cv2.circle(
                frame,
                (cx, cy),
                8,
                (0, 255, 255),
                -1
            )

            # -----------------------------
            # Index Finger Tip
            # -----------------------------

            index = hand.landmark[8]

            ix = int(index.x * w)
            iy = int(index.y * h)

            self.index_tip = (ix, iy)

            cv2.circle(
                frame,
                (ix, iy),
                10,
                (0, 255, 0),
                -1
            )

        return frame, landmarks