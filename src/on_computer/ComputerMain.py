import socket, json
from sys import orig_argv
from on_computer.computer_vision.ComputerVision import get_masks_from_camera, get_grid
from on_computer.pathfinding.Convert_to_node_grid import convert_to_grid
from on_computer.pathfinding.feedback import is_robot_position_correct
from pathfinding.PathfindingAlgorithm import grid, a_star
from positions.Positions import find_start_node, find_first_ball

#Creates a socket object, and established a connection to the robot

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.8.111"
port = 9999

def startRobot():
    client_socket.connect((host, port))
    command = 'PATH'
    client_socket.sendall(command.encode('utf-8'))

    masks = get_masks_from_camera()
    raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
    grid = convert_to_grid(raw_grid_data)
    robot_position = masks['blue']

    # below, y is first and x is second as the grid is a matrix not a cartesian plane

    start_node = find_start_node(robot_position, grid)# Function for diffing the calculated robot position with the camera robot position
        
    end_node = find_first_ball(grid)

    # Send the path to the robot
    path = a_star(grid, start_node, end_node)
    path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
    path_as_json = json.dumps(path_as_dictionaries)

    json_length = len(path_as_json)
    client_socket.sendall(json_length.to_bytes(4, 'big'))

    client_socket.sendall(path_as_json.encode('utf-8'))
    
    while(is_robot_position_correct(path, grid)):
        pass
    
    #Send the stop command to the robot

while True:
    startRobot()
    # Close the connection
    client_socket.close()

