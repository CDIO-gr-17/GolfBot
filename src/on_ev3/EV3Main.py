#!/usr/bin/env pybricks-micropython
import socket

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
                instruction, x, y = parts
                try:
                    x = int(x)
                    y = int(y)
                except ValueError:
                    print("Error: x or y cannot be converted to an integer. Received x='{x}', y='{y}'".format(x=x, y=y))
                    continue

                if instruction == 'DRIVE' or instruction == 'REVERSE':
                    robot.drivebase.straight(y)
                    print("Driving straight for: ", y)
                elif instruction == 'TURN':
                    print("Turning for: ", x)
                    robot.drivebase.turn(x)
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
