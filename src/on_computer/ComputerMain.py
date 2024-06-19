import socket
import json
from computer_vision.ComputerVision import get_masks_from_camera, get_grid
from pathfinding.Convert_to_node_grid import convert_to_grid
from pathfinding.feedback import is_robot_position_correct
from pathfinding.PathfindingAlgorithm import a_star
from positions.Positions import find_start_node, find_first_ball, get_robot_angle  # noqa: E501 <--- Is writting so Flake8 does not complain about line length
from helpers.end_of_path_pickup import distance_between, get_path_to_goal
from positions.Robot_direction import calculate_heading


# Creates a socket, and established a connection to the robot
host = "192.168.8.111"
port = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

def run_pickup(robot_pos, end_node): #Function for picking up the ball, when it has reached the end of the path
 print('ball is close')
 command = 'PICK'
 client_socket.sendall(command.encode('utf-8'))
#calculate heading from robot, to ball, to send
 new_heading = str(calculate_heading(robot_pos,end_node))
 client_socket.sendall(new_heading.encode('utf-8'))
 distance = str(distance_between(robot_pos, end_node))
 client_socket.sendall(distance.encode('utf-8'))

def score_balls():
     command = 'DEPO'
     client_socket.sendall(command.encode('utf-8')) #sends DEPO command to robot
     masks = get_masks_from_camera()
     raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
     grid = convert_to_grid(raw_grid_data)
     path = get_path_to_goal(grid,masks['green']) #gets path to goal, from a new grid.
     path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
     path_as_json = json.dumps(path_as_dictionaries)
     json_length = len(path_as_json)
     client_socket.sendall(json_length.to_bytes(4, 'big'))
     client_socket.sendall(path_as_json.encode('utf-8'))
     counter = 0


counter = 0
while True:

    command = 'PATH'
    client_socket.sendall(command.encode('utf-8'))

    masks = get_masks_from_camera()
    raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
    grid = convert_to_grid(raw_grid_data)
    robot_position = masks['green']
    robot_heading = get_robot_angle(masks, grid)
    print('The robots heading: ', robot_heading)

    # Find the robot, the first ball and a path between them
    start_node = find_start_node(robot_position, grid)
    end_node = find_first_ball(grid)
    path = a_star(grid, start_node, end_node)

    # The heading of the robot is sent to the robot
    if robot_heading is None:
        print('ERROR: No heading calcultated')
        # TODO: Handle this error
    else:
        client_socket.sendall(str(robot_heading).encode('utf-8'))

    # The path is sent to the robot
    if path is None:
        print('The algorithm could not find a path')
        # TODO: Handle this error
    else:
        print('The algorithm found a path!')
        path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
        path_as_json = json.dumps(path_as_dictionaries)
        json_length = len(path_as_json)
        client_socket.sendall(json_length.to_bytes(4, 'big'))  # We start by sending the length of the json string, so the robot knows how much data to expect # noqa: E501
        client_socket.sendall(path_as_json.encode('utf-8'))

    # While loop that runs until the robot is deemed to be of the path
    while (is_robot_position_correct(robot_heading, path, start_node)):
        print("Robot is on the right path")
        robot_step_done = client_socket.recv(4).decode('utf-8').strip()  # Here we wait for the robot to finish its current step # noqa: E501
        client_socket.send('GOOD'.encode('utf-8'))  # Send a positive confirmation to the robot, it can continue # noqa: E501
        response = client_socket.recv(7).decode('utf-8').strip()  # Wait for a response from the robot # noqa: E501
        print(response)

        # ONGOING means that the robot is still on the path, and we simply update the variables and receive a confirmation # noqa: E501
        if response == 'ONGOING':
            masks = get_masks_from_camera()
            raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])  # noqa: E501
            grid = convert_to_grid(raw_grid_data)
            robot_position = masks['green']
            start_node = find_start_node(robot_position, grid)
            confirmation = client_socket.recv(7).decode('utf-8').strip()
            print(confirmation)

            # HEADING means that the robot has done an adjustment of it's heading,
        # we calculate the new actual heading an send that to the robot and receive a confirmation # noqa: E501
        if response == 'HEADING':
            masks = get_masks_from_camera()
            raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])  # noqa: E501
            grid = convert_to_grid(raw_grid_data)
            robot_position = masks['green']
            robot_heading = get_robot_angle(masks, grid)
            client_socket.sendall(str(robot_heading).encode('utf-8'))
            confirmation = client_socket.recv(7).decode('utf-8').strip()

        if response == 'PICK':
            # if distance_to_ball <= 13 and counter == ball_array[counter] :
            masks = get_masks_from_camera()
            raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
            grid = convert_to_grid(raw_grid_data)

            robot_pos = masks['green']

            run_pickup(robot_pos, end_node)
            counter += 1



    # Send the stop command to the robot
    while True:
        course_notice = 'STOP'
        client_socket.sendall(course_notice.encode('utf-8'))
        response = client_socket.recv(7).decode('utf-8').strip()
        print(response)
        if response == 'STOPPED':
            break
