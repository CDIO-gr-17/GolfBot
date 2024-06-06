import math
import numpy as np
gridLength = 300 #cm
gridWidth = 300 #cm
gridSize = 5 #cm
cameraHeight = 200 / gridSize
robotHeight = 10 / gridSize

resolution = (int(gridLength/gridSize), int(gridWidth/gridSize))
grid = np.zeros(resolution)

#Find the middle of the grid
def find_middle(grid):
    rows, cols = grid.shape
    middle = (int(cols/2), int(rows/2))
    return middle

#Find the distance from the middle of the grid to a specific field
def find_distance_from_middle(grid, field):
    middle = find_middle(grid)
    distance = math.sqrt((field[0] - middle[0])**2 + (field[1] - middle[1])**2)
    return distance

#Find the angle of a specific field to the camera
def find_angle_to_field(grid, field):
    distance = find_distance_from_middle(grid, field)
    angle = math.atan(cameraHeight/distance)
    return angle

#Find the displacement of the robot, given the field position of the robot
def find_displacement_of_robot(grid, robotFieldPosition):
    angle = find_angle_to_field(grid, robotFieldPosition)
    displacement = robotHeight/math.tan(angle)
    return displacement

print(find_middle(grid))
robotFieldPosition = (0/gridSize,150/gridSize)
print(find_displacement_of_robot(grid, robotFieldPosition))