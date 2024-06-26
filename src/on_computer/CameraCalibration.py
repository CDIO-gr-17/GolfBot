from cv2.gapi import video
import numpy as np
import cv2
import glob
import pathlib
import yaml

x = 1280
y = 720
resolution = (x, y)

def get_calibration_data(filename="calibration_matrix.yaml"):
    with open(filename, "r") as f:
        data = yaml.safe_load(f)
    return np.array(data['camera_matrix']), np.array(data['dist_coeff'])

def capture_calibration_images():
    no_of_calibration_images = 20

    video_capture = cv2.VideoCapture(1, cv2.CAP_DSHOW) #Open camera WINDOWS OS
    #video_capture = cv.VideoCapture(0) #Open camera MAC OS

    path = 'images'
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    i = 0
    while i < no_of_calibration_images:
        ret, frame = video_capture.read()
        frame = cv2.resize(frame, resolution, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('capture calibration image - "q" to capture', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite(path + '/calib' + str(i) + '.jpg', frame)
            print("Image " + str(i) + " saved")
            i += 1

    video_capture.release()
    cv2.destroyAllWindows()


# Credit: https://nikatsanka.github.io/camera-calibration-using-opencv-and-python.html
def calibrate_camera():
    chessboardCorners = (6, 9)

    # Define the size of the squares in the chessboard, in meters
    squaresize = 0.05  # 2.3 cm = 0.023 m

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboardCorners[0]*chessboardCorners[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboardCorners[0],0:chessboardCorners[1]].T.reshape(-1,2)
    objp = objp * squaresize  # Multiply by the size of the squares to get the actual dimensions
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob(r'images/*.jpg')
    print(f'Found {len(images)} images.')

    # path = 'results'
    # pathlib.Path(path).mkdir(parents=True, exist_ok=True) 

    found = 0
    for fname in images:
        img = cv2.imread(fname) # Capture frame-by-frame
        #print(images[im_i])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, resolution, interpolation=cv2.INTER_NEAREST)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, chessboardCorners, None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            print('Found corners in image', fname)
            objpoints.append(objp)   # Certainly, every loop objp is the same, in 3D.
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)
            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, chessboardCorners, corners2, ret)
            found += 1
            cv2.imshow('img', img)
            cv2.waitKey(500)
            # if you want to save images with detected corners 
            # uncomment following 2 lines and lines 5, 18 and 19
            # image_name = path + '/calibresult' + str(found) + '.png'
            # cv2.imwrite(image_name, img)
        else:
            print('Corners not found in image', fname)

    print("Number of images used for calibration: ", found)

    # When everything done, release the capture
    # cap.release()
    cv2.destroyAllWindows()

    # calibration
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        frame = cv2.resize(frame, resolution, interpolation=cv2.INTER_NEAREST)

        # If frame is read correctly, ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Undistort the frame
        undistorted_frame = cv2.undistort(frame, mtx, dist, None, mtx)

        # Display the resulting frame
        cv2.imshow('Undistorted Video Capture - "q" to close', undistorted_frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) == ord('q'):
            break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


    # transform the matrix and distortion coefficients to writable lists
    data = {'camera_matrix': np.asarray(mtx).tolist(),
            'dist_coeff': np.asarray(dist).tolist()}

    # and save it to a file
    with open("calibration_matrix.yaml", "w") as f:
        yaml.dump(data, f)

#capture_calibration_images()
calibrate_camera()