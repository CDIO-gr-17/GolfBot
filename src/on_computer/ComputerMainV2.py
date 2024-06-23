from re import S
import socket
import json
import time
import copy
import threading
from pathfinding.feedback import is_robot_position_correct
from pathfinding.PathfindingAlgorithm import a_star
from positions.Positions import find_first_ball, find_start_node
from computer_vision.Camera import capture_frames
from computer_vision.ComputerVision import update_positions
import Globals as G
from ComputerController import ComputerController
from helpers.end_of_path_pickup import distance_between, get_path_to_goal

HOST = "192.168.8.111"
PORT = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

controller = ComputerController(client_socket)

#Assign thread to capture continous frames
threading.Thread(target=capture_frames).start()

while G.BIG_FRAME is None or G.SMALL_FRAME is None:
    time.sleep(0.2)

#Assign thread to update positions using CV
threading.Thread(target=update_positions).start()

# We are in danger of going on old data cause we dont check if a new position is found in pictures
# Dont really know if it is a problem, shouldnt be if recognition is good enough
while G.ROBOT_POSITION is None or G.ROBOT_HEADING is None or G.GRID is None or G.BALLS is None:
    print("robot pos: ", G.ROBOT_POSITION)
    print("balls: ", G.BALLS)
    time.sleep(0.2)

print(G.ROBOT_POSITION)
end_node = find_first_ball(G.GRID)
counter = 0
while True:
    print("LOOP")
    distance = 1000
    if G.BALLS is not None:
        distance = distance_between(G.ROBOT_POSITION, G.BALLS[0])

    grid_snap_shot =  copy.deepcopy(G.GRID)
    end_node = grid_snap_shot[end_node.y][end_node.x]
    start_node = grid_snap_shot[G.ROBOT_POSITION[1]][G.ROBOT_POSITION[0]]
    print("Start node: ", start_node)
    print("End node: ", end_node)
    path = a_star(grid_snap_shot, start_node, end_node)
    print("Path to first ball: ", path)

    if counter == 3:
        print("DEPO")
        goal_path = get_path_to_goal()
        path_as_tuples = [(node.x, node.y) for node in goal_path]
        controller.send_command('DEPO', {'heading': G.ROBOT_HEADING, 'path': path_as_tuples})
        while True:
            if not is_robot_position_correct(path, find_start_node()):
                controller.send_command('ABORT', {})
                break
            else:
                counter = 0
        continue

    elif distance < 25:
        print("PICK")
        controller.send_command('PICK', {'heading': G.ROBOT_HEADING, 'distance': distance})
        counter += 1
        del G.BALLS[0]

    elif counter < 3:
        print ('PATH')
        path_as_tuples = [(node.x, node.y) for node in path]
        print(path_as_tuples)
        controller.send_command('PATH', {'heading': G.ROBOT_HEADING, 'path': path_as_tuples})
        while(is_robot_position_correct(path, find_start_node())):
            pass
        controller.send_command('ABORT', {})
