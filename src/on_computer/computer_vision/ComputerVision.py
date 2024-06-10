import cv2 as cv
import numpy as np



#Kamera 0
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

x = 25
y = 25
resolution = (x, y) # Det skal vel ikke være kvadratisk?
mask_grid = np.zeros((resolution))

def write_pixel_grid(mask_red, mask_orange, mask_white, mask_green, matrix):
    obstacle_grid = matrix.copy()
    balls_grid = matrix.copy()
    goal_grid = matrix.copy()
    combined_grid = matrix.copy()
    rows, cols = mask_red.shape
    for i in range(rows):
        for j in range(cols):

            #Obstacle
            red_pixel_value = mask_red[i, j]
            #binary_value = 0 if pixel_value == 0 else 1 # Calculate binary value
            obstacle_binary_value = 0
            if red_pixel_value == 0:
                obstacle_binary_value = 0
            else:
                obstacle_binary_value = 1
            obstacle_grid[i][j] = obstacle_binary_value

            #Balls
            orange_pixel_value = mask_orange[i, j]
            white_pixel_value = mask_white[i, j]
            balls_binary_value = 0
            if orange_pixel_value != 0 or white_pixel_value != 0:
                balls_binary_value = 1
            balls_grid[i][j] = balls_binary_value

            #Goal
            green_pixel_value = mask_green[i, j]
            goal_binary_value = 0
            if green_pixel_value == 0:
                goal_binary_value = 0
            else:
                goal_binary_value = 1
            goal_grid[i][j] = goal_binary_value

            # Set the values in the combined grid
            if obstacle_grid[i][j] == 1:
                combined_grid[i][j] = 1
            elif balls_grid[i][j] == 1:
                combined_grid[i][j] = 2

    #print(algorithm.ball_detector(balls_grid))

    # Save the grids to files - Unneccessary should be removed, but might be nice for visualization and debugging
   # with open("grid_output/obstacle.txt", "w") as file:
   #     np.savetxt(file, obstacle_grid, fmt="%.0f")
    #with open("grid_output/balls.txt", "w") as file:
   #     np.savetxt(file, balls_grid, fmt="%.0f")
   # with open("grid_output/goal.txt", "w") as file:
   #     np.savetxt(file, goal_grid, fmt="%.0f")
    #with open("grid_output/combined_grid.txt", "w") as file:
     #   np.savetxt(file, combined_grid, fmt="%.0f")

    return combined_grid # Returns the combined grid

def display_grid(frame, mask):
    upscaled_resized_frame = cv.resize(mask, (x*7, y*7), interpolation=cv.INTER_NEAREST)
    upscaled_resized_frame_hsv = cv.resize(frame, (x*7, y*7), interpolation=cv.INTER_NEAREST)
    cv.imshow('', upscaled_resized_frame)

def get_grid():
    video_capture = cv.VideoCapture(0)
    
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
        
        display_grid(resized_frame, mask_white)
        grid = write_pixel_grid(mask_red, mask_orange, mask_white, mask_green, mask_grid)
        video_capture.release()
        cv.destroyAllWindows()
    return grid

#while True:
get_grid()  
#if cv.waitKey(1) & 0xFF == ord('q'): break
