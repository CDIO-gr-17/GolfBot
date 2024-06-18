import socket, json, time
from pathfinding.Convert_to_node_grid import convert_to_grid
from pathfinding.feedback import is_robot_position_correct
from pathfinding.PathfindingAlgorithm import a_star
from positions.Positions import find_start_node, find_first_ball, get_robot_angle
import threading
from computer_vision.Camera import capture_frames
from computer_vision.ComputerVision import update_positions


BIG_FRAME = None
SMALL_FRAME = None

#Assigne thread to capture continous frames
camera_thread = threading.Thread(target=capture_frames).start()

ROBOT_POSITION = None
ROBOT_HEADING = None
GRID = None
BALLS = None

while BIG_FRAME is None or SMALL_FRAME is None:
    time.sleep(0.2)

position_thread = threading.Thread(target=update_positions).start()

# We are in danger of going on old data cause we dont check if a new position is found in pictures
while ROBOT_POSITION is None or ROBOT_HEADING is None or GRID is None or BALLS is None:
    time.sleep(0.2)

time.sleep(20)


#Creates a socket object, and established a connection to the robot
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.8.111"
port = 9999

client_socket.connect((host, port))


while True:
    command = 'PATH'
    client_socket.sendall(command.encode('utf-8'))

    start_node = find_start_node(ROBOT_POSITION, GRID)# Function for diffing the calculated robot position with the camera robot position
    end_node = find_first_ball(GRID)

    # Send the path to the robot
    path = a_star(GRID, start_node, end_node)

    if path != None:
        print('Path: OK')
        path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
        path_as_json = json.dumps(path_as_dictionaries)
    else: print('The algorithm could not find a path')

    if ROBOT_HEADING == None:
        print('ERROR: No heading calcultated')
        exit()
    else:
        heading_as_string = str(ROBOT_HEADING)
        client_socket.sendall(heading_as_string.encode('utf-8'))

    json_length = len(path_as_json)
    client_socket.sendall(json_length.to_bytes(4, 'big'))

    client_socket.sendall(path_as_json.encode('utf-8'))

    while(is_robot_position_correct(ROBOT_HEADING, path, start_node)):
        print("correct")
        course_notice = 'KEEP'
        client_socket.sendall(course_notice.encode('utf-8'))
        response = client_socket.recv(7).decode('utf-8').strip()
        print(response)

        if response == 'ONGOING':
            start_node = find_start_node(ROBOT_POSITION, GRID)

        if response == 'HEADING':
            client_socket.sendall(str(ROBOT_HEADING).encode('utf-8'))



    # Send the stop command to the robot
    while True:
        course_notice = 'STOP'
        client_socket.sendall(course_notice.encode('utf-8'))
        response = client_socket.recv(7).decode('utf-8').strip()
        print(response)
        if response == 'STOPPED':
            break
