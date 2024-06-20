import json
import time
import errno
from RobotBuilder import Robot

class RobotController:
    def __init__(self, socket):
        self.socket = socket
        while True:
            try:
                self.client_socket, self.client_address = self.socket.accept()
                break
            except OSError as e:
                if hasattr(e, 'errno') and e.errno != errno.EAGAIN:
                    raise
            time.sleep(0.1)
        self.robot = Robot()

    def recieve_command(self, size = 1024):
        try:
            return self.client_socket.recv(size).decode('utf-8').strip()
        except BlockingIOError:
            return ""


    def handle_command(self, command):
        try:
            command_data = json.loads(command)
        except json.JSONDecodeError:
            print("Invalid command format")
            return

        cmd = command_data.get('command')
        params = command_data.get('payload')

        if cmd == "DEPO":
            if not isinstance(params, dict) or 'heading' not in params or 'path' not in params:
                print("Invalid parameters for DEPO command")
                return
            self.robot.move_through_path(params['path'], params['heading'], self)
            self.robot.deposit()
        elif cmd == "PICK":
            if not isinstance(params, dict) or 'heading' not in params or 'distance' not in params:
                print("Invalid parameters for PICK command")
                return
            self.robot.turn_to_heading(params['heading'])
            self.robot.pickup_ball(params['distance'])
        elif cmd == "PATH":
            if not isinstance(params, dict) or 'heading' not in params or 'path' not in params:
                print("Invalid parameters for PATH command")
                return
            self.robot.move_through_path(params['path'], params['heading'], self)
        else:
            print("Invalid command")
