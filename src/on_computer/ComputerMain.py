import socket
import json
import time
import threading
from pathfinding.feedback import is_robot_position_correct
from pathfinding.PathfindingAlgorithm import a_star
from positions.Positions import find_start_node, find_first_ball
from computer_vision.Camera import capture_frames
from computer_vision.ComputerVision import update_positions
import Globals as G
import cv2 as cv

# Assign thread to capture continous frames
threading.Thread(target=capture_frames).start()

while G.BIG_FRAME is None or G.SMALL_FRAME is None:
    time.sleep(0.2)

# Assign thread to update positions using CV
threading.Thread(target=update_positions).start()

# while True:
#     if G.SMALL_FRAME is not None:
#         cv.imshow('frame', G.BIG_FRAME)
#         print(G.ROBOT_POSITION)
#         if cv.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit the loop
#             break

# We are in danger of going on old data cause we dont check if a new position is found in pictures
# Dont really know if it is a problem, shouldnt be if recognition is good enough
while G.ROBOT_POSITION is None or G.ROBOT_HEADING is None or G.GRID is None or G.BALLS is None:
    time.sleep(0.2)

# Creates a socket object, and established a connection to the robot
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "192.168.8.111"
PORT = 9999
client_socket.connect((HOST, PORT))

while True:
    COMMAND = 'PATH'
    client_socket.send(COMMAND.encode('utf-8'))

    start_node = find_start_node()  # Function for diffing the calculated robot position with the camera robot position
    end_node = find_first_ball(G.GRID)

    print(len(G.GRID))

    # Send the path to the robot
    path = a_star(G.GRID, start_node, end_node)

    if path is not None:
        print('Path: OK')
        path_as_touples = [(node.x,node.y) for node in path]
        path_as_json = json.dumps(path_as_touples)
    else:
        print('The algorithm could not find a path')

    if G.ROBOT_HEADING is None:
        print('ERROR: No heading calcultated')
        exit()
    else:
        heading_as_string = str(int(G.ROBOT_HEADING))
        client_socket.send(heading_as_string.encode('utf-8'))

    json_length = len(path_as_json)
    client_socket.send(json_length.to_bytes(4, 'big'))

    client_socket.send(path_as_json.encode('utf-8'))

    while is_robot_position_correct(G.ROBOT_HEADING, path, start_node):
        start_node = find_start_node()

    # Send the stop command to the robot
    print('attempting to stop robot')
    while True:
        COURSE_NOTICE = 'STOP'
        client_socket.send(COURSE_NOTICE.encode('utf-8'))
        response = client_socket.recv(7).decode('utf-8').strip()
        print(response)
        if response == 'STOPPED':
            break
