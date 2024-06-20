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
        parts = command.split()
        if not parts:
            return


        #We could instead do the below with
        # def send_message(command, payload):
        #     message = json.dumps({'command': command, 'payload': payload})
        #     client_socket.send((message + "\n").encode('utf-8'))
        #But on computer and then put it together as json object and acces everything with ['command'] and ['payload']
        # and easier to understand and more secure to use with None and shit like that


        cmd = parts[0]
        params = parts[1:]
        print("cmd:", cmd)
        print("params", params)


        if cmd == "DEPO": 
            heading = int(params[-1])
            json_string = ' '.join(params[:-1])
            path_as_tuples = json.loads(json_string)
            self.robot.move_through_path(path_as_tuples, heading, self)
            self.robot.deposit()
        elif cmd == "PICK":
            self.robot.turn_to_heading(params[0])
            self.robot.pickup_ball(params[1])
        elif cmd == "PATH":
            heading = int(params[-1])
            #json_string = ' '.join(params[:-1])
            path_as_tuples = json.loads(params[0])
            self.robot.move_through_path(path_as_tuples, heading, self)
        else:
            return

