import socket
import json
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from RobotBuilder import Robot

class RobotController:
    def __init__(self, socket):
        self.socket = socket
        self.client_socket, self.client_address = socket.accept()
        self.robot = Robot()

    def recieve_command(self, size = 1024):
        return self.client_socket.recv(size).decode('utf-8').strip()


    def handle_command(self, command):
        parts = command.split()
        if not parts:
            return

        cmd = parts[0]
        params = parts[1:]


        if cmd == "DEPO":
            self.robot.move_through_path(params[0], params[1], self)
            self.robot.deposit()
        elif cmd == "PICK":
            self.robot.turn_to_heading(params[0])
            self.robot.pickup_ball(params[1])
        elif cmd == "PATH":
            heading = int(params[-1])
            json_string = ' '.join(params[:-1])
            path_as_dictionaries = json.loads(json_string)
            path = [(d['x'], d['y']) for d in path_as_dictionaries]
            self.robot.move_through_path(path, heading, self)
        else:
            return
