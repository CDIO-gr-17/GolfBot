#!/usr/bin/env pybricks-micropython

# import PathfindingAlgorithm
# from PathfindingAlgorithm import grid, start, end, Node
import json
import re
import EV3Connector
from RobotBuilder import Robot
from Heading import Heading

s = EV3Connector.establish_socket()
robot = Robot()

clientsocket, adress = s.accept()
print('Connection established')

print('running...')

def recv_all(sock, length): #Helper function to receive exactly 'length' bytes from 'sock'
    data = bytearray()
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

while True:
    # Establish a connection

    # Receive the command
    command = clientsocket.recv(4).decode('utf-8').strip()

    if command == 'PATH':
        print('Recieved command: PATH')

        currentHeading_as_string = clientsocket.recv(3).decode('utf-8').strip()
        currentHeading = int(currentHeading_as_string)
        print(currentHeading)

        length_data = clientsocket.recv(4)

        if length_data:
            length = int.from_bytes(length_data, 'big')

            # Receive the path
            path_data = recv_all(clientsocket, length).decode('utf-8')

            path_as_dictionaries = json.loads(path_data)

            path = [(d['x'], d['y']) for d in path_as_dictionaries]

            print(path)

            currentX = path[0][0]
            currentY = path[0][1]

            print(currentX, currentY, currentHeading)

            path_length = len(path)
            robot.move_through_path(path[0],path[path_length-1],currentHeading, path, clientsocket)

            print("Awaiting new command...")
    elif command == "PICK":
        print('Recieved command: PICK')
        recieved_heading = clientsocket.recv(4).decode('utf-8').strip()
        recieved_distance = clientsocket.recv(4).decode('utf-8').strip()
        print(recieved_heading)
        clientsocket.close()
        
        currentHeading = int(recieved_heading)
        print(currentHeading)

        robot.turn_to_heading(currentHeading)

        robot.pickup_ball(recieved_distance)

    elif command == 'DEPO':
        print ('Recieved command: DEPO')

        path_length_in_bytes =  clientsocket.recv(4)

        path_length = int.from_bytes(path_length_in_bytes, 'big')
        path_data = recv_all(clientsocket, path_length).decode('utf-8')
        path_as_dictionaries = json.loads(path_data)

        path = [(d['x'], d['y']) for d in path_as_dictionaries]
    
        currentX = path[0][0]
        currentY = path[0][1]

        print(currentX, currentY, currentHeading)
        path_length = len(path)
        robot.move_through_path(path[0],path[path_length-1],currentHeading, path, clientsocket)
        robot.deposit()







    #clientsocket.close()