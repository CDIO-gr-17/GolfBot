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
        ret, frame = cap.read()
        if ret:
            # Define the threshold
            # threshold = 250   # change the value as needed

            # Apply gamma correction to pixels above the threshold
            # gamma_high = 0.01  # gamma value for high intensity pixels, change the value as needed
            # gamma_low = 1.0  # gamma value for low intensity pixels, change the value as needed
            # invGamma_high = 1.0 / gamma_high
            # invGamma_low = 1.0 / gamma_low
            # table = np.array([((i / 255.0) ** invGamma_high) * 255 if i > threshold else ((i / 255.0) ** invGamma_low) * 255 for i in np.arange(0, 256)]).astype("uint8")
            # result = cv.LUT(frame, table)
            # We are not making a margin around the area so maybe we still get bright spots that is abov
            # Apply the CLAHE algorithm to the frame
            # ycrcb = cv.cvtColor(frame, cv.COLOR_BGR2YCrCb)
            # y, cr, cb = cv.split(ycrcb)
            # clahe = cv.createCLAHE(clipLimit=1000, tileGridSize=(8, 8))
            # y = clahe.apply(y)
            # ycrcb = cv.merge((y, cr, cb))
            # result = cv.cvtColor(ycrcb, cv.COLOR_YCrCb2BGR)

            G.BIG_FRAME = frame
            G.SMALL_FRAME = cv.resize(G.BIG_FRAME, (320, 180))

        # Wait for 200 ms
        # time.sleep(0.1)

    # Release the camera when done
    cap.release()
