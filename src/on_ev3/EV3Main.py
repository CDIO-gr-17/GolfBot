#!/usr/bin/env pybricks-micropython

import json
import sys
import EV3Connector

from RobotBuilder import Robot

print('running...')
print(sys.version_info)  # Check python version

clientsocket = None
s = None

try:
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
        robot.buffer = clientsocket.recv(4).decode('utf-8').strip()

        if 'PATH' in robot.buffer:
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
            robot.step = 0
        while 'PATH' in robot.buffer:
            robot.buffer = robot.buffer.replace('PATH', '')

        if 'PICK' in robot.buffer:
            print('Recieved command: PICK')

            distance_to_ball = float(clientsocket.recv(40).decode('utf-8').rstrip('\x00'))
            heading_to_ball = int(clientsocket.recv(3).decode('utf-8').rstrip('\x00'))
            print('The robot should be at', heading_to_ball, 'degrees')
            robot.current_heading = int(clientsocket.recv(3).decode('utf-8').rstrip('\x00'))
            print('The robot is at', robot.current_heading, 'degrees')
            print('Picking up ball')
            robot.pickup_ball(distance_to_ball, heading_to_ball)
            clientsocket.send('STOPPED'.encode('utf-8'))
            robot.step = 0
            while 'PICK' in robot.buffer:
                robot.buffer = robot.buffer.replace('PICK', '')

        if 'GOAL' in robot.buffer:
            print('Recieved command: GOAL')

        data_length = clientsocket.recv(4)
        if data_length is not None:
            length = int.from_bytes(data_length, 'big')
            path_data = recv_all(clientsocket, length).decode('utf-8')
            path = [(node[0], node[1]) for node in json.loads(path_data)]
            print(path)

                initialX = path[0][0]
                initialY = path[0][1]

            path_length = len(path)
            robot.move_through_path(path[0], path[path_length-1], 0, path, clientsocket)
            if robot.step == len(path):
                robot.deposit()
            robot.step = 0
        while 'GOAL' in robot.buffer:
            robot.buffer = robot.buffer.replace('GOAL', '')
        clientsocket.send('STOPPED'.encode('utf-8'))

except Exception as e:
    print('An error occurred:', e)
finally:
    if clientsocket:
        clientsocket.close()
    if s:
        s.close()