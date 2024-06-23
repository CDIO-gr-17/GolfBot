import copy
import json
import socket
import threading
import time

import Globals as G

from pathfinding.feedback import is_robot_position_correct
from pathfinding.PathfindingAlgorithm import a_star
from positions.Positions import find_start_node, find_first_ball, sort_balls_by_distance
from computer_vision.Camera import capture_frames
from computer_vision.ComputerVision import update_positions
from helpers.end_of_path_pickup import distance_between
from helpers.get_path_to_goal import get_path_to_goal
from pathfinding.PathfindingAlgorithm import a_star
from pathfinding.feedback import is_robot_position_correct
from positions.Positions import find_first_ball, find_start_node
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

print(G.ROBOT_POSITION, G.ROBOT_HEADING, G.BALLS[0])
end_node = G.GRID[G.BALLS[0][1]][G.BALLS[0][0]] #Is it possible to do this?


balls_picked_up = 0

while True:
    # If statement for depositing the balls in goal
    if balls_picked_up == 3:
        client_socket.send('GOAL'.encode('utf-8'))
        goal_path = get_path_to_goal()
        to_goal_start_node = goal_path[0]
        if goal_path is None:
            print('The algorithm could not find a path to the goal')
            time.sleep(5)
        else:
            path_as_tuples = [(node.x, node.y) for node in goal_path]
            print(path_as_tuples)
            path_as_json = json.dumps(path_as_tuples)
            json_length = len(path_as_json)
            client_socket.send(json_length.to_bytes(4, 'big'))
            client_socket.send(path_as_json.encode('utf-8'))
            balls_picked_up = 0
            while is_robot_position_correct(G.ROBOT_HEADING, goal_path, to_goal_start_node):
                client_socket.send('KEEP'.encode('utf-8'))
                time.sleep(1)
                to_goal_start_node = find_start_node()
            print('attempting to stop robot')
            for i in range(10):
                client_socket.send('STOP'.encode('utf-8'))
            response = client_socket.recv(7).decode('utf-8').strip()

    # If statement for picking up balls
    elif distance_between(G.ROBOT_POSITION, (end_node.x, end_node.y)) < 50:
        if G.BALLS is not None:
            heading_to_ball = calculate_heading(G.ROBOT_POSITION, G.BALLS[0])
            distance = distance_between(G.ROBOT_POSITION, G.BALLS[0])
            client_socket.send('PICK'.encode('utf-8'))
            client_socket.send(str(distance).encode('utf-8'))
            client_socket.send(str(int(heading_to_ball)).encode('utf-8'))
            client_socket.send(str(int(G.ROBOT_HEADING)).encode('utf-8'))
            response = client_socket.recv(7).decode('utf-8').strip()
            balls_picked_up += 1
            end_node = G.GRID[G.BALLS[0][1]][G.BALLS[0][0]]  # We make sure the robot is going to the next ball

    # The robot will follow a path to the first ball in G.BALLS
    if balls_picked_up != 3:
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
            path_as_touples = [(node.x, node.y) for node in path[:-5]]
            path_as_json = json.dumps(path_as_touples)
            json_length = len(path_as_json)
            client_socket.send(json_length.to_bytes(4, 'big'))
            client_socket.send(path_as_json.encode('utf-8'))

        while is_robot_position_correct(G.ROBOT_HEADING, path, start_node):
            client_socket.send('KEEP'.encode('utf-8'))
            time.sleep(1)
            start_node = find_start_node()
            if (distance_between(G.ROBOT_POSITION, (end_node.x, end_node.y)) < 50):
                break

        # Send the stop command to the robot
        print('attempting to stop robot')
        for i in range(10):
            client_socket.send('STOP'.encode('utf-8'))

        response = client_socket.recv(7).decode('utf-8').strip()
        print(response)
