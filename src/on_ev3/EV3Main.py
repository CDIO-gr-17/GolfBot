#!/usr/bin/env pybricks-micropython

# import PathfindingAlgorithm
# from PathfindingAlgorithm import grid, start, end, Node
import json
import EV3Connector
from RobotBuilder import Robot
from Heading import Heading

s = EV3Connector.establish_socket()
robot = Robot()

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
    clientsocket, adress = s.accept()
    print('Connection established')

    # Receive the command
    command = clientsocket.recv(4).decode('utf-8').strip()

    if command == 'PATH':
        print('Recieved command')

        clientsocket.settimeout(2) # now the socket will only wait 10 seconds for a response, this is utilized in the off_course_notice condition

        length_data = clientsocket.recv(4)

        if length_data:
            length = int.from_bytes(length_data, 'big')
            
            currentHeading = Heading.NORTH  # Assuming initial heading is north

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
                    response = "STOPPED"
                    print('Stopped due to drift')
                    #clientsocket.send(response.encode('utf-8'))
                    break

    clientsocket.close()