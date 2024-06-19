class RobotController:
    def __init__(self, socket):
        self.socket = socket

    def send_command(self, command):
        self.socket.sendall(command.encode('utf-8'))

    def recieve_command(self):
        return self.socket.recv(1024).decode('utf-8').strip()
