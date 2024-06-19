class ComputerController:
    def __init__(self, socket):
        self.socket = socket

    def send_command(self, command, *params):
        # Format the command and parameters into a message
        message = command
        for param in params:
            message += ' ' + str(param)

        # Convert the message to bytes and send it over the socket
        self.socket.sendall(message.encode('utf-8'))

    def recieve_command(self):
        return self.socket.recv(1024).decode('utf-8').strip()
