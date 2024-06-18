import time
import socket, json
from sys import orig_argv
from computer_vision.ComputerVision import get_masks_from_camera, get_grid
from pathfinding.Convert_to_node_grid import convert_to_grid
from pathfinding.feedback import is_robot_position_correct
from pathfinding.PathfindingAlgorithm import a_star
from positions.Positions import find_start_node, find_first_ball, get_robot_angle
from helpers.end_of_path_pickup import distance_between
from positions.Robot_direction import calculate_heading


#Creates a socket object, and established a connection to the robot

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.8.111"
port = 9999

client_socket.connect((host, port))

def degrees_to_heading(degrees):
    if degrees != None:
        # Define the boundaries for each heading
        if (degrees >= 337.5) or (degrees < 22.5):
            return "NRTH"
        elif 22.5 <= degrees < 67.5:
            return "NREA"
        elif 67.5 <= degrees < 112.5:
            return "EAST"
        elif 112.5 <= degrees < 157.5:
            return "SOWE"
        elif 157.5 <= degrees < 202.5:
            return "SOUT"
        elif 202.5 <= degrees < 247.5:
            return "SOWE"
        elif 247.5 <= degrees < 292.5:
            return "WEST"
        elif 292.5 <= degrees < 337.5:
            return "NOWE"
        else:
            return "ERRO"
    else:
        return "ERRO<ç"

def run_pickup(robot_pos, end_node):
    print('ball is close')
    command = 'PICK'
    client_socket.sendall(command.encode('utf-8'))
    #calculate heading for ball
    #new_heading = degrees_to_heading(calculate_heading(robot_pos,end_node))
    client_socket.sendall("WEST".encode('utf-8'))




counter = 0
while True:
    masks = get_masks_from_camera()
    raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
    grid = convert_to_grid(raw_grid_data)
    robot_position = masks['green']
    robot_heading = degrees_to_heading(get_robot_angle(masks, grid))
    print('The robots heading: ', robot_heading)
    # below, y is first and x is second as the grid is a matrix not a cartesian plane

    start_node = find_start_node(robot_position, grid)# Function for diffing the calculated robot position with the camera robot position

    end_node = find_first_ball(grid)

    #distance_to_ball = distance_between(robot_position, end_node)
    # if distance_to_ball < 5 or 1==1:

    if True:
        run_pickup(robot_position, end_node)
        counter += 1

    else:
        command = 'PATH'
        client_socket.sendall(command.encode('utf-8'))

        # Send the path to the robot
        path = a_star(grid, start_node, end_node)

        if path != None: print('Path: OK')
        else: print('The algorithm could not find a path')

        path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
        path_as_json = json.dumps(path_as_dictionaries)

        client_socket.sendall(robot_heading.encode('utf-8'))

        json_length = len(path_as_json)
        client_socket.sendall(json_length.to_bytes(4, 'big'))

        client_socket.sendall(path_as_json.encode('utf-8'))

        while(is_robot_position_correct(path, grid)):
            print("correct")
            pass

        # Send the stop command to the robot
        while True:
            off_course_notice = 'STOP'
            client_socket.sendall(off_course_notice.encode('utf-8'))
            response = client_socket.recv(7).decode('utf-8').strip()
            print(response)
            if response == 'STOPPED':
                break








