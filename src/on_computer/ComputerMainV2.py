import socket
import json
import time
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
    time.sleep(0.2)

print(G.ROBOT_POSITION)

counter = 0
while True:
    print("LOOP")
    first_ball = find_first_ball(G.GRID)
    distance = distance_between(G.ROBOT_POSITION, G.BALLS[0])
    path = a_star(G.GRID, find_start_node(), first_ball)

    if counter == 3:
        print("DEPO")
        goal_path = get_path_to_goal()
        path_as_json = json.dumps(goal_path)
        controller.send_command('DEPO', path, G.ROBOT_HEADING)
        while(is_robot_position_correct(path, find_start_node())):
            controller.send_command('CONTINUE')
        counter = 0

    elif distance < 10:
        print("PICK")
        controller.send_command('PICK', G.ROBOT_HEADING, distance)
        counter += 1

    elif counter < 3:
        path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
        path_as_json = json.dumps(path_as_dictionaries)
        controller.send_command('PATH', path_as_json, G.ROBOT_HEADING)
        while(is_robot_position_correct(path, find_start_node())):
            pass
        controller.send_command('ABORT')
