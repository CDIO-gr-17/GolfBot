import PathfindingAlgorithm
from PathfindingAlgorithm import grid, start, end, Node
import ujson as json
import EV3Connector
import Robot

socket = EV3Connector.establish_socket()
robot = Robot()

while True:
    # Establish a connection
    clientsocket = socket.accept()

    # Receive the command
    command = clientsocket.recv(1024).decode('utf-8')

    if command == 'PATH':
        # Receive the path
        path = json.loads(clientsocket.recv(1024).decode('utf-8'))

        currentHeading = Heading.NORTH  # Assuming initial heading is north

        currentX = path[0]['x']
        currentY = path[0]['y']

        print(currentX, currentY, currentHeading)
        
        for node in path[1:]:  # Skip the starting node as it's the current position
            currentHeading = moveToPoint(node['x'], node['y'], currentX, currentY, currentHeading)
            ev3.speaker.beep()  # Optional: beep after each move
            currentX, currentY = node['x'], node['y']  # Update current position

    clientsocket.close()