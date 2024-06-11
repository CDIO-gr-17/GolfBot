import cv2 as cv
import numpy as np

x = 250
y = 140
resolution = (x, y)
mask_grid = np.zeros((resolution))

def get_robot_head(mask_green):
    coordinates = np.argwhere(mask_green != 0)
    if len(coordinates) == 0:
        return None
    return coordinates[0] # Returns the first green pixel found, but should maybe be the middle pixel //TODO

def get_robot_tail(mask_blue):
    coordinates = np.argwhere(mask_blue != 0)
    if len(coordinates) == 0:
        return None
    return coordinates[0] # Returns the first green pixel found, but should maybe be the middle pixel //TODO

def get_grid(mask_red, mask_orange, mask_white):
    obstacle_coordinates = np.argwhere(mask_red != 0)
    ball_coordinates = np.argwhere(np.logical_or(mask_orange != 0, mask_white != 0))

    combined_grid = np.zeros_like(mask_red)

    combined_grid[obstacle_coordinates[:, 0], obstacle_coordinates[:, 1]] = 1
    combined_grid[ball_coordinates[:, 0], ball_coordinates[:, 1]] = 2

    np.savetxt('combined_grid.txt', combined_grid, fmt='%d')

    return combined_grid

def get_masks_from_camera():
    video_capture = cv.VideoCapture(1, cv.CAP_DSHOW)

    #Define color ranges
    red_lower_1 = np.array([0, 100, 20], dtype="uint8")
    red_upper_1 = np.array([5, 255, 255], dtype="uint8")

    red_lower_2 = np.array([170, 100, 20], dtype="uint8")
    red_upper_2 = np.array([180, 255, 255], dtype="uint8")

    orange_lower = np.array([15, 100, 20], dtype="uint8")
    orange_upper = np.array([25, 255, 255], dtype="uint8")

    white_lower = np.array([0, 0, 220], dtype="uint8")
    white_upper = np.array([180, 100, 255], dtype="uint8")

    green_lower = np.array([50, 100, 20], dtype="uint8")
    green_upper = np.array([70, 255, 255], dtype="uint8")

    green_lower = np.array([65, 50, 20], dtype="uint8")
    green_upper = np.array([85, 255, 255], dtype="uint8")

    blue_lower = np.array([100, 150, 20], dtype="uint8")
    blue_upper = np.array([110, 255, 255], dtype="uint8")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Camera not detected")

        elif ret:
            blur_frame = cv.GaussianBlur(frame, (17, 17), 0) #Add blur
            hsv_frame = cv.cvtColor(blur_frame, cv.COLOR_BGR2HSV) #Convert from RGB to HSV
            resized_frame = cv.resize(hsv_frame, resolution, interpolation=cv.INTER_NEAREST) #Apply the resolution specified

            # Create masks for red, green, blue, orange and white
            mask_red_1 = cv.inRange(resized_frame, red_lower_1, red_upper_1)
            mask_red_2 = cv.inRange(resized_frame, red_lower_2, red_upper_2)
            mask_red = cv.bitwise_or(mask_red_1, mask_red_2)
            mask_green = cv.inRange(resized_frame, green_lower, green_upper)
            mask_blue = cv.inRange(resized_frame, blue_lower, blue_upper)
            mask_robot = cv.bitwise_or(mask_green, mask_blue) #Combine blue and green to see the robot
            mask_orange = cv.inRange(resized_frame, orange_lower, orange_upper)
            mask_white = cv.inRange(resized_frame, white_lower, white_upper)

            #Apply dilation
            obstacle_kernel = np.ones((15, 15), np.uint8)
            ball_kernel = np.ones((3, 3), np.uint8)
            mask_white = cv.dilate(mask_white, ball_kernel)
            mask_orange = cv.dilate(mask_orange, ball_kernel)
            mask_red = cv.dilate(mask_red,obstacle_kernel)

            masks = {
                'red': mask_red,
                'orange': mask_orange,
                'white': mask_white,
                'green': mask_green,
                'blue': mask_blue
            }

            get_grid(mask_red, mask_orange, mask_white)

            cv.imshow('ImageWindow', mask_white)
            if cv.waitKey(1) & 0xFF == ord('q'): break
    video_capture.release()
    cv.destroyAllWindows()
    return masks

get_masks_from_camera()