import socket
import PathfindingAlgorithm
from PathfindingAlgorithm import grid, Node
import json
from ArrayGenerator import create_border_array
from computer_vision.ComputerVision import get_grid, get_masks_from_camera, get_robot_pos_with_mask
from computer_vision.Displacement import move_point
from computer_vision.Robot_direction import calculate_heading

masks = get_masks_from_camera()

raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
ball_node = PathfindingAlgorithm.node

def convert_to_grid(data):
    rows = len(data)
    cols = len(data[0])
    grid = []

    for i in range(rows):
        row_nodes = []
        for j in range(cols):
            node = Node(grid, j, i)
            element = data[i][j]
            if element == 1:
                node.type = 'wall'
            elif element == 0:
                node.type = 'road'
            elif element == 2:
                node.type = 'ball'
            row_nodes.append(node)
        grid.append(row_nodes)

    return grid

grid = convert_to_grid(raw_grid_data)

# below, y is first and x is second as the grid is a matrix not a cartesian plane

robot_head = get_robot_pos_with_mask(masks['blue'])
robot_real_position = move_point(robot_head, grid)
robot_tail = get_robot_pos_with_mask(masks['green'])
robot_real_tail = move_point(robot_tail,grid)
robot_angle = calculate_heading(robot_real_tail,robot_real_position)
print(robot_angle)


start_node = grid[int(robot_real_position[0])][int(robot_real_position[1])]

def find_first_ball(grid):
    for row in grid:
        for node in row:
            if node.type == 'ball':
                return node
    return None

# Function for diffing the calculated robot position with the camera robot position
def is_robot_position_correct(robot_path, camera_robot_position, robot_step):
    return robot_path[robot_step].x == camera_robot_position[0] and robot_path[robot_step].y == camera_robot_position[1]
    
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
