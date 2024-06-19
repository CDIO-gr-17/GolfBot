import time
import cv2 as cv
import Globals as G

# Function to capture frames
def capture_frames():
    # Open the camera
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)


    while True:
        # Capture a frame
        G.BIG_FRAME = cap.read()
        G.SMALL_FRAME = cv.resize(G.BIG_FRAME, (320, 180))

        # Wait for 200 ms
        time.sleep(0.1)

    # Release the camera when done
    cap.release()