class ComputerController:
    def __init__(self, socket):
        self.socket = socket

    def send_command(self, command, *params):
    # Format the command and parameters into a message
        message = command
        for param in params:
            # If the parameter is a JSON string, enclose it in quotes
            if isinstance(param, str) and (param.startswith('{') or param.startswith('[')):
                message += ' "' + param + '"'
            else:
                message += ' ' + str(param)

        # Convert the message to bytes and send it over the socket
        self.socket.sendall((message + "\n").encode('utf-8'))

    def recieve_command(self):
        return self.socket.recv(2048).decode('utf-8').strip()
