import cv2 as cv
import numpy as np



#Kamera 0
red_lower_1 = np.array([0, 200, 20], dtype="uint8")
red_upper_1 = np.array([5, 255, 255], dtype="uint8")

red_lower_2 = np.array([170, 200, 20], dtype="uint8")
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

x = 300
y = 170
resolution = (x, y) # Det skal vel ikke være kvadratisk?
mask_grid = np.zeros((resolution))

def get_robot_head(mask_green):
    coordinates = np.argwhere(mask_green != 0)
    if len(coordinates) == 0:
        return None
    return coordinates[0] # Return the first green pixel found, but should be the middle //TODO

def get_robot_tail(mask_blue):
    coordinates = np.argwhere(mask_blue != 0)
    if len(coordinates) == 0:
        return None
    return coordinates[0] # Return the first green pixel found, but should be the middle //TODO


#This should be rewritten to use np.argwhere instead of nested for loops
def create_combined_grid(mask_red, mask_orange, mask_white, matrix):
    obstacle_coordinates = set(map(tuple, np.argwhere(mask_red != 0)))
    ball_coordinates = set(map(tuple, np.argwhere(np.logical_or(mask_orange != 0, mask_white != 0))))
    combined_grid = matrix.copy()

    for i in range(combined_grid.shape[0]):
        for j in range(combined_grid.shape[1]):
            if (i, j) in obstacle_coordinates:
                combined_grid[i, j] = 1
            elif (i, j) in ball_coordinates:
                combined_grid[i, j] = 2
            else:
                combined_grid[i, j] = 0
        
    #np.savetxt('combined_grid.txt', combined_grid, fmt='%d')

    return combined_grid

def display_grid(mask):
    upscaled_resized_frame = cv.resize(mask, (x*7, y*7), interpolation=cv.INTER_NEAREST)
    cv.imshow('ImageWindow', upscaled_resized_frame)

def get_grid():
    video_capture = cv.VideoCapture(1, cv.CAP_DSHOW)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("No frame")

        #Make the frame blurry
        blur_frame = cv.GaussianBlur(frame, (17, 17), 0)
        #Make the frame hsv
        hsv_frame = cv.cvtColor(blur_frame, cv.COLOR_BGR2HSV)
        #Make the frame
        resized_frame = cv.resize(hsv_frame, resolution, interpolation=cv.INTER_NEAREST)

        # Create masks for red, green, blue
        mask_red_1 = cv.inRange(resized_frame, red_lower_1, red_upper_1)
        mask_red_2 = cv.inRange(resized_frame, red_lower_2, red_upper_2)
        mask_red = cv.bitwise_or(mask_red_1, mask_red_2)
        mask_green = cv.inRange(resized_frame, green_lower, green_upper)
        mask_blue = cv.inRange(resized_frame, blue_lower, blue_upper)
        mask_orange = cv.inRange(resized_frame, orange_lower, orange_upper)
        mask_white = cv.inRange(resized_frame, white_lower, white_upper)

        ret, mask = cv.threshold(resized_frame, 200, 255, cv.THRESH_BINARY) #Hvad gør den her linje?
        if ret:
            #kernel = np.ones((5, 5), np.uint8) #den binære repræsentation af et billede
            #mask_cleaned = cv.morphologyEx(mask_to_use, cv.MORPH_OPEN, kernel) #mask isolere arealer i et billede
            #mask_cleaned = cv.morphologyEx(mask_cleaned, cv.MORPH_CLOSE, kernel) #siger nej tak til farver og siger ja tak til HVID
            #contours, hierarchy = cv.findContours(mask_to_use, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) #hierarchy er moralsk support her
            obstacle_kernel = np.ones((15, 15), np.uint8)
            ball_kernel = np.ones((3, 3), np.uint8)
            mask_white = cv.dilate(mask_white, ball_kernel)
            mask_orange = cv.dilate(mask_orange, ball_kernel)
            mask_red = cv.dilate(mask_red,obstacle_kernel)

            upscaled_resized_frame = cv.resize(mask_white, (x*2, y*2), interpolation=cv.INTER_NEAREST)
            grid = create_combined_grid(mask_red, mask_orange, mask_white, mask_grid)
        #display_grid(frame)
        cv.imshow('ImageWindow', upscaled_resized_frame)
        if cv.waitKey(1) & 0xFF == ord('q'): break
    video_capture.release()
    cv.destroyAllWindows()
    return grid



get_grid()
#if cv.waitKey(1) & 0xFF == ord('q'): break


def get_robot_position_and_heading():
    heading = 'NORTH'
    grid  = create_combined_grid(mask_red, mask_orange, mask_white, mask_grid)
    blue_square = grid[1][1]
    green_square = grid[1][2]
    if (blue_square[0] > green_square[0]):
        heading = 'NORTH'
    if (blue_square[1]< green_square[1]):
        heading = 'EAST'
    if (blue_square[0] < green_square[0]):
        heading = 'SOUTH'
    if (blue_square[1] > green_square[1]):
        heading = 'WEST'

    pos = (green_square , heading)
    return pos
