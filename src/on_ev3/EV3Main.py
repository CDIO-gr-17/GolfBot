#!/usr/bin/env pybricks-micropython

import json
import sys
import EV3Connector

from RobotBuilder import Robot

print('running...')
print(sys.version_info)  # Check python version

# Setup the connection
s = EV3Connector.establish_socket()
robot = Robot()
clientsocket, adress = s.accept()
print('Connection established')


def recv_all(sock, length):  # Helper function to receive exactly 'length' bytes from 'sock'
    data = bytearray()
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


while True:
    print("Awaiting command...")
    # Receive a command
    command = clientsocket.recv(4).decode('utf-8').strip()

    if command == 'PATH':
        print('Recieved command: PATH')

        initial_heading = int(clientsocket.recv(3).decode('utf-8').rstrip('\x00'))
        print('Initial heading: ', str(initial_heading))
        data_length = clientsocket.recv(4)

        if data_length is not None:
            length = int.from_bytes(data_length, 'big')
            path_data = recv_all(clientsocket, length).decode('utf-8')
            path = [(node[0], node[1]) for node in json.loads(path_data)]

            initialX = path[0][0]
            initialY = path[0][1]

            path_length = len(path)
            robot.move_through_path(path[0], path[path_length-1], initial_heading, path, clientsocket)

    if command == 'PICK':
        print('Recieved command: PICK')

        distance_to_ball = float(clientsocket.recv(4).decode('utf-8').rstrip('\x00'))
        heading_to_ball = int(clientsocket.recv(3).decode('utf-8').rstrip('\x00'))

        print('Picking up ball')
        robot.pickup_ball(distance_to_ball, heading_to_ball)
