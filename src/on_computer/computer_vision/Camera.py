import cv2 as cv
import time

# Function to capture frames
def capture_frames():
    global BIG_FRAME
    global SMALL_FRAME
    # Open the camera
    cap = cv.VideoCapture(0)
    org_width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    org_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

    while True:
        # Capture a frame
        cap.set(cv.CAP_PROP_FRAME_WIDTH, org_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, org_height)
        ret, BIG_FRAME = cap.read()
        cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 180)
        ret, SMALL_FRAME = cap.read()


        # Wait for 200 ms
        time.sleep(0.2)

    # Release the camera when done
    cap.release()