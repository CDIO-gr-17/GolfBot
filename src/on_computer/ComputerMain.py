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

#Assign thread to capture continous frames
threading.Thread(target=capture_frames).start()

while G.BIG_FRAME is None or G.SMALL_FRAME is None:
    time.sleep(0.2)

#Assign thread to update positions using CV
threading.Thread(target=update_positions).start()

while True:
    if G.SMALL_FRAME is not None:
        cv.imshow('frame', G.BIG_FRAME)
        print(G.ROBOT_POSITION)
        if cv.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit the loop
            break

# We are in danger of going on old data cause we dont check if a new position is found in pictures
# Dont really know if it is a problem, shouldnt be if recognition is good enough
while G.ROBOT_POSITION is None or G.ROBOT_HEADING is None or G.GRID is None or G.BALLS is None:
    time.sleep(0.2)



time.sleep(20)
cv.destroyAllWindows()


#Creates a socket object, and established a connection to the robot
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "192.168.8.111"
PORT = 9999
client_socket.connect((HOST, PORT))


counter = 0
while True:
    COMMAND = 'PATH'
    client_socket.sendall(COMMAND.encode('utf-8'))

    start_node = find_start_node()# Function for diffing the calculated robot position with the camera robot position
    end_node = find_first_ball(G.GRID)

    # Send the path to the robot
    path = a_star(G.GRID, start_node, end_node)

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
    else: print('The algorithm could not find a path')

    if G.ROBOT_HEADING is None:
        print('ERROR: No heading calcultated')
        exit()
    else:
        heading_as_string = str(G.ROBOT_HEADING)
        client_socket.sendall(heading_as_string.encode('utf-8'))

    json_length = len(path_as_json)
    client_socket.sendall(json_length.to_bytes(4, 'big'))

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
            start_node = find_start_node()

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
        COURSE_NOTICE = 'STOP'
        client_socket.sendall(COURSE_NOTICE.encode('utf-8'))
        response = client_socket.recv(7).decode('utf-8').strip()
        print(response)
        if response == 'STOPPED':
            break
