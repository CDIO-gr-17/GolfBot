import cv2 as cv
import numpy as np

def ball_detector(grid):
  """
  Identifies clusters of ones in a 2D grid and counts the number of balls.

  Args:
      grid: A 2D numpy array representing the grid (0s and 1s).

  Returns:
      The number of balls (clusters) found in the grid.
  """

  rows, cols = grid.shape
  visited = np.zeros_like(grid, dtype=bool)  # Keep track of visited cells
  ball_count = 0

  for i in range(rows):
    for j in range(cols):
      if grid[i, j] == 1 and not visited[i, j]:
        # Found a new ball (unvisited 1)
        ball_count += 1

        # Use a stack for iterative exploration
        stack = [(i, j)]
        while stack:
          row, col = stack.pop()
          visited[row, col] = True

          # Explore neighbors (up, down, left, right) within grid boundaries
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < grid.shape[0] and 0 <= new_col < grid.shape[1] and grid[new_row, new_col] == 1 and not visited[new_row, new_col]:
              stack.append((new_row, new_col))  # Add neighbor to stack for exploration

  return ball_count

def dfs(grid, visited, row, col):
  """
  Performs Depth-First Search to explore a cluster of connected ones.

  Args:
      grid: The 2D grid.
      visited: A boolean array to track visited cells.
      row: The current row index.
      col: The current column index.
  """

  # Mark current cell as visited
  visited[row, col] = True

  # Explore neighbors (up, down, left, right) within grid boundaries
  for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    new_row, new_col = row + dr, col + dc
    if 0 <= new_row < grid.shape[0] and 0 <= new_col < grid.shape[1] and grid[new_row, new_col] == 1 and not visited[new_row, new_col]:
      dfs(grid, visited, new_row, new_col)  # Recursive call for neighbor


videoCapture = cv.VideoCapture(1, cv.CAP_DSHOW)


#Kamera 0
red_lower1 = np.array([0, 100, 20], dtype="uint8")
red_upper1 = np.array([5, 255, 255], dtype="uint8")

red_lower2 = np.array([170, 100, 20], dtype="uint8")
red_upper2 = np.array([180, 255, 255], dtype="uint8")

orange_lower = np.array([15, 100, 20], dtype="uint8")
orange_upper = np.array([25, 255, 255], dtype="uint8")

white_lower = np.array([0, 0, 220], dtype="uint8")
white_upper = np.array([180, 100, 255], dtype="uint8")

green_lower = np.array([50, 100, 20], dtype="uint8")
green_upper = np.array([70, 255, 255], dtype="uint8")

x = 100
y = 100
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

    #print(ball_detector(balls_grid))

    with open("gridOutput/Obstacle.txt", "w") as file:
        np.savetxt(file, obstacle_grid, fmt="%.0f")
    with open("gridOutput/Balls.txt", "w") as file:
        np.savetxt(file, balls_grid, fmt="%.0f")
    with open("gridOutput/Goal.txt", "w") as file:
        np.savetxt(file, goal_grid, fmt="%.0f")
    with open("gridOutput/CombinedGrid.txt", "w") as file:
        np.savetxt(file, combined_grid, fmt="%.0f")

    return obstacle_grid, balls_grid, goal_grid, combined_grid # Return the grids // Is it actually possible to do it like this?

while True:
    ret, frame = videoCapture.read()
    if not ret: break 

    #Make the frame blurry
    blurFrame = cv.GaussianBlur(frame, (17, 17), 0)
    #Make the frame hsv
    hsvFrame = cv.cvtColor(blurFrame, cv.COLOR_BGR2HSV)
    #Make the frame
    resizedFrame = cv.resize(hsvFrame, resolution, interpolation=cv.INTER_NEAREST)

    # Create masks for red, green, blue
    mask_red1 = cv.inRange(resizedFrame, red_lower1, red_upper1)
    mask_red2 = cv.inRange(resizedFrame, red_lower2, red_upper2)
    mask_red = cv.bitwise_or(mask_red1, mask_red2)
    mask_green = cv.inRange(resizedFrame, green_lower, green_upper)
    mask_orange = cv.inRange(resizedFrame, orange_lower, orange_upper)
    mask_white = cv.inRange(resizedFrame, white_lower, white_upper)

    ret, mask = cv.threshold(resizedFrame, 200, 255, cv.THRESH_BINARY)
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
        display_mask = mask_red

        upscaledResizedFrame = cv.resize(display_mask, (x*7, y*7), interpolation=cv.INTER_NEAREST)
        upscaledResizedFrameHsv = cv.resize(resizedFrame, (x*7, y*7), interpolation=cv.INTER_NEAREST)
        write_pixel_grid(mask_red, mask_orange, mask_white, mask_green, mask_grid)

    cv.imshow('', upscaledResizedFrame)
    if cv.waitKey(1) & 0xFF == ord('q'): break

videoCapture.release()
cv.destroyAllWindows()