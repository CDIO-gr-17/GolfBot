#!/usr/bin/env pybricks-micropython
import socket
import time

from RobotBuilderReworked import Robot

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '192.168.8.111'
PORT = 9999
server_socket.bind((HOST, PORT))
server_socket.listen(1)

robot = Robot()

print('Waiting for a connection...')
connection, client_address = server_socket.accept()

try:
    print('Connection from', client_address)

    while True:
        print('Waiting for instructions...')
        data = connection.recv(1024).decode('utf-8')
        if data:
            parts = data.split()
            if len(parts) == 3:
                instruction, heading, distance = parts
                try:
                    heading = int(heading)
                    distance = int(distance)
                except ValueError:
                    print("Error: x or y cannot be converted to an integer. Received x='{x}', y='{y}'".format(x=heading, y=distance))
                    continue

                if instruction == 'DRIVE' or instruction == 'REVERSE':
                    robot.drivebase.straight(distance)
                    print("Driving straight for: ", distance)
                elif instruction == 'PICKUP':
                    print('The robot will turn to pickup balls: ', heading)
                    robot.drivebase.turn(heading)
                    robot.front_motor.run(1000)
                    robot.drivebase.straight(distance)
                    robot.front_motor.stop
                elif instruction == 'TURN':
                    print("Turning for: ", heading)
                    robot.drivebase.turn(heading)
                elif instruction == 'EJECT':
                    print("Ejecting balls")
                    robot.drivebase.turn(heading)
                    robot.drivebase.straight(distance)
                    #  robot.drivebase.settings(100, 200)
                    robot.front_motor.run(-1000)
                    for i in range(3):
                        acc = 50
                        robot.drivebase.straight(-acc)
                        robot.drivebase.straight(acc)
                        acc += 20


            else:
                print("Error: Expected 3 parts from the split operation, got {}: {}".format(len(parts), parts))
        else:
            break
finally:
    connection.close()


###############

# print('Waiting for a connection...')
# connection, client_address = server_socket.accept()

# try:
#     print('Connection from', client_address)

#     while True:
#         data = connection.recv(1024).decode('utf-8')
#         if data:
#             instruction, x, y = data.split()
#             if instruction == 'DRIVE':
#                 robot.drivebase.straight(int(y))
#             elif instruction == 'REVERSE':
#                 robot.drivebase.straight(int(y))
#             elif instruction == 'TURN':
#                 robot.drivebase.turn(int(x))
#         else:
#             break
# finally:
#     connection.close()
