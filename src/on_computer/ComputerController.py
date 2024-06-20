import json
class ComputerController:
    def __init__(self, socket):
        self.socket = socket

    def send_command(self, command, payload):
    # Create the command data
        command_data = {
            'command': command,
            'payload': payload
        }

        # Convert the command data to a JSON string
        command_string = json.dumps(command_data)

    # Convert the command string to bytes and send it over the socket
        self.socket.sendall((command_string + "\n").encode('utf-8'))

    def recieve_command(self):
        return self.socket.recv(2048).decode('utf-8').strip()
