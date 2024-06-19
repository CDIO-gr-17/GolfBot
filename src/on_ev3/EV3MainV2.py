#!/usr/bin/env pybricks-micropython

# The above line is how the EV# determines that this is it's main python script

from src.on_ev3.RobotController import RobotController
from src.on_ev3.EV3Connector import establish_socket
from src.on_ev3.RobotBuilder import Robot

socket = establish_socket()
controller = RobotController(socket)

command = controller.recieve_command()

controller.handle_command(command)

