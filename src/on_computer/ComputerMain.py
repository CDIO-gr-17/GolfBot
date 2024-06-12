import socket

from cv2 import filterHomographyDecompByVisibleRefpoints
import PathfindingAlgorithm
from PathfindingAlgorithm import grid, Node
import json
from ArrayGenerator import create_border_array
from computer_vision.ComputerVision import get_grid, get_masks_from_camera, get_robot_pos_with_mask
from computer_vision.Displacement import move_point
from computer_vision.Robot_direction import calculate_heading
from Convert_to_node_grid import convert_to_grid

masks = get_masks_from_camera()

raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
ball_node = PathfindingAlgorithm.node
grid = convert_to_grid(raw_grid_data)

# below, y is first and x is second as the grid is a matrix not a cartesian plane


def find_start_node():
    robot_camera_position = get_robot_pos_with_mask(masks['blue'])
    robot_real_position = move_point(robot_camera_position, grid) #Accounting for displacement
    if (robot_real_position is None):
        print("Robot position is not found")
        return
    return grid[int(robot_real_position[0])][int(robot_real_position[1])]

def get_robot_angle():
    robot_camera_tail = get_robot_pos_with_mask(masks['green'])
    robot_real_tail = move_point(robot_camera_tail,grid)
    robot_angle = calculate_heading(robot_real_tail , find_start_node() )
    if robot_angle is None:
        print("Robot angle is not found")
        return
    return robot_angle

def find_first_ball(grid):
    for row in grid:
        for node in row:
            if node.type == 'ball':
                return node
    return None


start_node = find_start_node()
end_node = find_first_ball(grid)

print(start_node.x, start_node.y)
print(end_node.x, end_node.y)

#Creates a socket object, and established a connection to the robot

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.8.111"
port = 9999

client_socket.connect((host, port))

command = 'PATH'
client_socket.sendall(command.encode('utf-8'))

# Send the path to the robot
path = PathfindingAlgorithm.a_star(grid, start_node, end_node)
path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
path_as_json = json.dumps(path_as_dictionaries)

#print(path_as_dictionaries)


json_length = len(path_as_json)
client_socket.sendall(json_length.to_bytes(4, 'big'))

client_socket.sendall(path_as_json.encode('utf-8'))

# Close the connection
client_socket.close()
