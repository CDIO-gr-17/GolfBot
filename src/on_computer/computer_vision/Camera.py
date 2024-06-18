import cv2 as cv
import time
import Globals as G

# Function to capture frames
def capture_frames():
    # Open the camera
    cap = cv.VideoCapture(0)
    org_width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    org_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    while True:
        # Capture a frame
        ret, G.BIG_FRAME = cap.read()
        G.SMALL_FRAME = cv.resize(G.BIG_FRAME, (320, 180))


        # Wait for 200 ms
        time.sleep(0.1)

    # Release the camera when done
    cap.release()