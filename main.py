import cv2

from detection.hand_detector import HandDetector
from detection.gesture_detector import GestureDetector
from controllers.game_controller import GameController
from utils.fps import FPS

# Open Webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Cannot open webcam")
    exit()

# Create Objects
hand_detector = HandDetector()
gesture_detector = GestureDetector()
game_controller = GameController()
fps_counter = FPS()

while True:

    success, frame = camera.read()

    if not success:
        break

    # Flip Frame
    frame = cv2.flip(frame, 1)

    # Detect Hand
    frame, landmarks = hand_detector.detect(frame)

    gesture = "NO HAND"

    if landmarks:

        # Detect Gesture
        gesture = gesture_detector.recognize(landmarks)

        # Perform Game Action
        game_controller.press_key(gesture)

    # FPS
    fps = fps_counter.calculate()

    # Show FPS
    cv2.putText(
        frame,
        f"FPS : {fps}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Show Gesture
    cv2.putText(
        frame,
        f"Gesture : {gesture}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    # Display
    cv2.imshow("Virtual Game Controller", frame)

    # Press Q to Exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()