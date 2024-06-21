import time
import cv2 as cv
import Globals as G

# Function to capture frames
def capture_frames():
    # Open the camera
    cap = cv.VideoCapture(1,cv.CAP_DSHOW) #CHANGE FRO MAC TO WINDOWS HERE

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        # Capture a frame
        ret, G.BIG_FRAME = cap.read()
        if ret:
            G.SMALL_FRAME = cv.resize(G.BIG_FRAME, (320, 180))

        # Wait for 200 ms
        time.sleep(0.1)

    # Release the camera when done
    cap.release()
