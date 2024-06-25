import socket
import threading
import time
import copy
import Globals as G

from pathfinding.PathfindingAlgorithm import a_star
from positions.Positions import find_start_node, find_first_ball
from computer_vision.Camera import capture_frames
from computer_vision.ComputerVision import update_positions
from helpers.get_path_to_goal import get_path_to_goal
from positions.Robot_direction import calculate_heading
from path_navigator import move_through_path, send_instruction


#  Helper function to move the robot through a path
def move_robot(path, robot_mode):
    path_as_tuples = [(node.x, node.y) for node in path]
    if robot_mode == 'BALL':
        reduced_path_as_touples = path_as_tuples[:-20]
    else:
        reduced_path_as_touples = path_as_tuples
    return move_through_path(path_as_tuples[1], path_as_tuples[-1], reduced_path_as_touples, robot_mode)


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
G.CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "192.168.8.111"
PORT = 9999
G.CLIENT_SOCKET.connect((HOST, PORT))

balls_picked_up = 0

while True:
    if balls_picked_up == 3:
        goal_path = get_path_to_goal()
        if goal_path is None:
            print('The algorithm could not find a path to the goal')
            send_instruction('REVERSE', 0, -15)
            time.sleep(0.5)
        else:
            if move_robot(goal_path, 'GOAL'):
                balls_picked_up = 0
            else:
                print('Recalculating path to goal...')
    else:
        start_node = find_start_node()
        end_node = find_first_ball(G.GRID)

        grid_copy = copy.deepcopy(G.GRID)
        end_node_copy = grid_copy[end_node.y][end_node.x]
        start_node_copy = grid_copy[start_node.y][start_node.x]
        path = a_star(grid_copy, start_node_copy, end_node_copy)
        if path is None:
            print('No path found, waiting...')
            send_instruction('REVERSE', 0, -20)
            time.sleep(0.5)
        else:
            if move_robot(path, 'BALL'):
                balls_picked_up += 1
            else:
                print('Recalculating path to ball...')