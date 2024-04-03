#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
import socket

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = "192.168.8.111"
port = 9999

# Bind to the port
serversocket.bind((host, port))

# Queue up to 5 requests
serversocket.listen(5)

while True:
    # Establish a connection
    clientsocket,addr = serversocket.accept()
    
    # Receive the command
    command = clientsocket.recv(1024).decode('utf-8')
    
    if command == 'FORWARD':
        # Code to move the robot forward
        # Go forward for one meter.
        robot.straight(1000)
        ev3.speaker.beep()
        pass
    elif command == 'BACKWARD':
        # Go backwards for one meter.
        # Code to move the robot backward
        robot.straight(-1000)
        ev3.speaker.beep()
        pass

    clientsocket.close()