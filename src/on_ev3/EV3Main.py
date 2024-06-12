#!/usr/bin/env pybricks-micropython

import EV3Connector
from RobotBuilder import Robot

s = EV3Connector.establish_socket()
robot = Robot()

print('running...')

while True:
    # Establish a connection
    clientsocket, adress = s.accept()
    print('Connection established')

    # Receive the command
    command = clientsocket.recv(4).decode('utf-8').strip()

    if command == 'FRWD':
        robot.moveForward()
    elif command == 'BACK':
        robot.moveBackward()
    elif command == 'LEFT':
        robot.turnLeft()
    elif command == 'RGHT':
        robot.turnRight()

    clientsocket.close()