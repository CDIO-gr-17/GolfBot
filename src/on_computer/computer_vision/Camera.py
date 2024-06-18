import cv2 as cv
import time
import Globals as G

# Function to capture frames
def capture_frames():
    # Open the camera
    cap = cv.VideoCapture(0)
    org_width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    org_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    while True:
        # Capture a frame
        cap.set(cv.CAP_PROP_FRAME_WIDTH, org_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, org_height)
        ret, G.BIG_FRAME = cap.read()
        if not cap.set(cv.CAP_PROP_FRAME_WIDTH, 320):
            print("Error: Could not set the width of the frame.")
        if not cap.set(cv.CAP_PROP_FRAME_HEIGHT, 180):
            print("Error: Could not set the height of the frame.")
        ret, G.SMALL_FRAME = cap.read()


        # Wait for 200 ms
        time.sleep(0.5)

    # Release the camera when done
    cap.release()