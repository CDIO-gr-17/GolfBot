import math
import numpy as np
grid_length = 300 #cm
grid_width = 300 #cm
grid_size = 5 #cm
camera_height = 200 / grid_size
robot_height = 10 / grid_size

resolution = (int(grid_length/grid_size), int(grid_width/grid_size))
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
    angle = math.atan(camera_height/distance)
    return angle

def find_angle_from_centre_to_robot(grid, robot_field_position):
    middle = find_middle(grid)
    angle = math.atan((robot_field_position[0]-middle[0])/(robot_field_position[1]-middle[1]))
    return angle

#Find the displacement of the robot, given the field position of the robot
def find_displacement_of_robot(grid, robot_field_position):
    angle = find_angle_to_field(grid, robot_field_position)
    displacement = robot_height/math.tan(angle)
    return displacement


print(find_middle(grid))
robot_field_position = (0/grid_size,150/grid_size)
print(find_displacement_of_robot(grid, robot_field_position))