import time
import socket, json
from sys import orig_argv
from computer_vision.ComputerVision import get_masks_from_camera, get_grid
from pathfinding.Convert_to_node_grid import convert_to_grid
from pathfinding.feedback import is_robot_position_correct
from pathfinding.PathfindingAlgorithm import a_star
from positions.Positions import find_start_node, find_first_ball, get_robot_angle

#Creates a socket object, and established a connection to the robot
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.8.111"
port = 9999

client_socket.connect((host, port))

while True:
    

    command = 'PATH'
    client_socket.sendall(command.encode('utf-8'))

    masks = get_masks_from_camera()
    raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
    grid = convert_to_grid(raw_grid_data)
    robot_position = masks['green']
    robot_heading = get_robot_angle(masks, grid)
    print('The robots heading: ', robot_heading)

    start_node = find_start_node(robot_position, grid)# Function for diffing the calculated robot position with the camera robot position
    end_node = find_first_ball(grid)

    # Send the path to the robot
    path = a_star(grid, start_node, end_node)

    if path != None:
        print('Path: OK')
        path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
        path_as_json = json.dumps(path_as_dictionaries)
    else: print('The algorithm could not find a path')

    if robot_heading == None:
        print('ERROR: No heading calcultated')
        exit()
    else:
        heading_as_string = str(robot_heading)
        client_socket.sendall(heading_as_string.encode('utf-8'))

    json_length = len(path_as_json)
    client_socket.sendall(json_length.to_bytes(4, 'big'))

    client_socket.sendall(path_as_json.encode('utf-8'))

    while(is_robot_position_correct(robot_heading, path, start_node)):
        print("correct")
        course_notice = 'KEEP'
        client_socket.sendall(course_notice.encode('utf-8'))
        response = client_socket.recv(7).decode('utf-8').strip()
        print(response)

        if response == 'ONGOING':
            masks = get_masks_from_camera()
            raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
            grid = convert_to_grid(raw_grid_data)
            robot_position = masks['green']
            start_node = find_start_node(robot_position, grid)

        if response == 'HEADING':
            masks = get_masks_from_camera()
            raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
            grid = convert_to_grid(raw_grid_data)
            robot_position = masks['green']
            robot_heading = get_robot_angle(masks, grid)
            client_socket.sendall(str(robot_heading).encode('utf-8'))

        if response == 'PICKUP!':
            #insert the method for picking up the ball
            break


    
    # Send the stop command to the robot
    while True:
        course_notice = 'STOP'
        client_socket.sendall(course_notice.encode('utf-8'))
        response = client_socket.recv(7).decode('utf-8').strip()
        print(response)
        if response == 'STOPPED':
            break
