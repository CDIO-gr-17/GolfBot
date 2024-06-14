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

def string_to_heading(heading_str):
    if heading_str is 'ER':
        print('Error in heading')
        exit()
    switcher = {
        "NO": Heading.NORTH,
        "NE": Heading.NORTHEAST,
        "EA": Heading.EAST,
        "SE": Heading.SOUTHEAST,
        "SO": Heading.SOUTH,
        "SW": Heading.SOUTHWEST,
        "WE": Heading.WEST,
        "NW": Heading.NORTHWEST
    }
    
    return switcher.get(heading_str.upper(), None)

def recv_all(sock, length): #Helper function to receive exactly 'length' bytes from 'sock'
    data = bytearray()
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

while True:
    print("going")
    # Establish a connection

    # Receive the command
    command = clientsocket.recv(4).decode('utf-8').strip()

    if command == 'PATH':
        print('Recieved command')

        recieved_heading = clientsocket.recv(2).decode('utf-8').strip()
        print(recieved_heading)


        currentHeading = string_to_heading(recieved_heading)
        print(currentHeading)

        length_data = clientsocket.recv(4)

        if length_data:
            length = int.from_bytes(length_data, 'big')

            # Receive the path
            path_data = recv_all(clientsocket, length).decode('utf-8')

            path = json.loads(path_data)


            currentX = path[0]['x']
            currentY = path[0]['y']

            print(currentX, currentY, currentHeading)

            for node in path[1:]:  # Skip the starting node as it's the current position
                currentHeading = robot.moveToPoint(node['x'], node['y'], currentX, currentY, currentHeading)
                currentX, currentY = node['x'], node['y']  # Update current position
                off_course_notice = clientsocket.recv(4).decode('utf-8').strip()
                if off_course_notice == 'STOP':
                    print('Stopped due to drift')
                    break
                
    #clientsocket.close()