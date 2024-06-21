import socket
import json
import time
import threading
import copy
import Globals as G

from pathfinding.feedback import is_robot_position_correct
from pathfinding.PathfindingAlgorithm import a_star
from positions.Positions import find_start_node, find_first_ball
from computer_vision.Camera import capture_frames
from computer_vision.ComputerVision import update_positions
from helpers.end_of_path_pickup import distance_between
from positions.Robot_direction import calculate_heading

# Assign thread to capture continous frames
threading.Thread(target=capture_frames).start()

while G.BIG_FRAME is None or G.SMALL_FRAME is None:
    time.sleep(0.2)

# Assign thread to update positions using CV
threading.Thread(target=update_positions).start()

# We are in danger of going on old data cause we dont check if a new position,
# is found in pictures. Dont really know if it is a problem,
# shouldnt be if recognition is good enough
while G.ROBOT_POSITION is None or G.ROBOT_HEADING is None or G.GRID is None or G.BALLS is None:
    print('Heading: ', G.ROBOT_HEADING)
    print('The robot position: ', G.ROBOT_POSITION)
    print('The ball position: ', G.BALLS)
    time.sleep(0.2)

# Creates a socket object, and established a connection to the robot
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "192.168.8.111"
PORT = 9999
client_socket.connect((HOST, PORT))

end_node = find_first_ball(G.GRID)

amount_balls_left = len(G.BALLS)

while True:
    # If statement for depositing the balls in goal
    if len(G.BALLS) == amount_balls_left - 3:
        ammount_balls_left = len(G.BALLS)
        COMMAND = 'GOAL'
        # TODO: Implement the goal scoring method.

    # If statement for picking up balls
    elif distance_between(G.ROBOT_POSITION, G.BALLS[0]) < 50:
        if G.BALLS is not None:
            heading_to_ball = calculate_heading(G.ROBOT_POSITION, G.BALLS[0])
            distance = distance_between(G.ROBOT_POSITION, G.BALLS[0])
            client_socket.send('PICK'.encode('utf-8'))
            client_socket.send(str(distance).encode('utf-8'))

    # The robot will follow a path to the first ball in G.BALLS
    else:
        client_socket.send('PATH'.encode('utf-8'))

        start_node = find_start_node()  # Function for diffing the calculated robot position with the camera robot position

        if G.ROBOT_HEADING is None:
            print('ERROR: No heading calcultated')
        else:
            heading_as_string = str(int(G.ROBOT_HEADING))
            client_socket.send(heading_as_string.encode('utf-8'))
            print('Heading send')

        grid_copy = copy.deepcopy(G.GRID)
        end_node_copy = grid_copy[end_node.y][end_node.x]
        start_node_copy = grid_copy[start_node.y][start_node.x]
        path = a_star(grid_copy, start_node_copy, end_node_copy)

        if path is None:
            print('The algorithm could not find a path')
        else:
            print('Path: OK')
            path_as_touples = [(node.x, node.y) for node in path]
            path_as_json = json.dumps(path_as_touples)
            json_length = len(path_as_json)
            client_socket.send(json_length.to_bytes(4, 'big'))
            client_socket.send(path_as_json.encode('utf-8'))

        while is_robot_position_correct(G.ROBOT_HEADING, path, start_node):
            client_socket.send('KEEP'.encode('utf-8'))
            time.sleep(1)
            start_node = find_start_node()

        # Send the stop command to the robot
        print('attempting to stop robot')
        for i in range(10):
            client_socket.send('STOP'.encode('utf-8'))

        response = client_socket.recv(7).decode('utf-8').strip()
        print(response)
