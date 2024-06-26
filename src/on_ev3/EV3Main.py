#!/usr/bin/env pybricks-micropython
import socket
import time

from RobotBuilder import Robot

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
                    robot.front_motor.run(-2000)
                    time.sleep(1)
                    robot.drivebase.straight(distance)
                    for i in range(5):
                        timer = 0.7
                        robot.drivebase.drive(1000, 0)
                        time.sleep(timer)
                        robot.drivebase.stop()
                        robot.drivebase.drive(-950, 0)
                        time.sleep(timer)
                        robot.drivebase.stop()

            else:
                print("Error: Expected 3 parts from the split operation, got {}: {}".format(len(parts), parts))
        else:
            break
finally:
    connection.close()
