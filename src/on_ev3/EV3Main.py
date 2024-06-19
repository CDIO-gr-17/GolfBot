#!/usr/bin/env pybricks-micropython

# The above line is how the EV# determines that this is it's main python script
from RobotController import RobotController
from EV3Connector import establish_socket

socket = establish_socket()
controller = RobotController(socket)

while True:

    command = controller.recieve_command()

    controller.handle_command(command)

