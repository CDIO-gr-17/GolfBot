#!/usr/bin/env pybricks-micropython

# The above line is how the EV# determines that this is it's main python script
from RobotController import RobotController
from EV3Connector import establish_socket

socket = establish_socket()
controller = RobotController(socket)
buffer = ""

while True:
    data = controller.recieve_command()
    if data:
        buffer += data
        while "\n" in buffer:
            command, buffer = buffer.split("\n", 1)
            controller.handle_command(command)

