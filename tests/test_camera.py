import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open webcam.")
    exit()

width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = camera.get(cv2.CAP_PROP_FPS)

print("Camera Information")
print("------------------")
print(f"Width  : {width}")
print(f"Height : {height}")
print(f"FPS    : {fps}")

camera.release()