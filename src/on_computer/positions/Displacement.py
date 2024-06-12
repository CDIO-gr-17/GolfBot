import math
import numpy as np
# grid_length = 300 #cm
# grid_width = 300 #cm

# resolution = (300,170)
# grid = np.zeros(resolution)

grid_size = 5 #cm
camera_height = 200 / grid_size
robot_height = 10 / grid_size

#Find the middle of the grid$
def find_middle(grid):
    rows = len(grid)
    cols = len(grid[0])
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

def move_point(robot_position, grid):
    # if  robot_position is None or grid is None:
    #     print("Robot position or grid is not found")
    #     return

    # Convert points to numpy arrays
    distance = find_displacement_of_robot(grid, robot_position)
    point_b = find_middle(grid)
    a = np.array(robot_position)
    b = np.array(point_b)

    # Calculate the vector from point_a to point_b
    vector = b - a

    # Calculate the distance between the points
    vector_length = np.linalg.norm(vector)

    # Normalize the vector (unit vector in the direction of point_b)
    unit_vector = vector / vector_length

    # Scale the unit vector by the desired distance
    move_vector = unit_vector * distance

    # Calculate the new point
    new_point = a + move_vector

    return new_point.tolist()


# # Example usage
# point_a = [170, 150]

# new_point = move_point(point_a, grid)
# print(new_point)
