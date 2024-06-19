

import json

import EV3Connector

from RobotBuilder import Robot


# Establish a connection to the computer
s = EV3Connector.establish_socket()
clientsocket, address = s.accept()
print('Connection established')

# Initialize the robot
robot = Robot()

print('running...')


# Helper function to receive exactly 'length' bytes from 'sock'
def recv_all(sock, length):
    data = bytearray()
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


# The main loop of the EV3's program
while True:
    command = clientsocket.recv(4).decode('utf-8').strip()  # Receive a command

    # If the command is PATH, the EV3 will receive a path from the computer, and navigate through it. # noqa: E501
    # It is in this part of the code that the EV3 can recieve different commands from the computer # noqa: E501
    if command == 'PATH':
        print('Recieved command: ', command)
        print('Recieved command: PATH')

        currentHeading = int(clientsocket.recv(3).decode('utf-8').rstrip('\x00'))  # '.rstrip('\x00')' removes all trailing null/none bytes # noqa: E501
        length_data = clientsocket.recv(4)  # Receive the length of the path data # noqa: E501

        if length_data is not None:
            length = int.from_bytes(length_data, 'big')
            path_data = recv_all(clientsocket, length).decode('utf-8')  # Receive the path # noqa: E501
            path_as_dictionaries = json.loads(path_data)

            path = [(d['x'], d['y']) for d in path_as_dictionaries]  # Convert the path to a list of tuples # noqa: E501

            currentX = path[0][0]
            currentY = path[0][1]

            print(currentX, currentY, currentHeading)

            path_length = len(path)
            robot.move_through_path(path[0], path[path_length-1], currentHeading, path, clientsocket)  # Navigation through the path starts here # noqa: E501

            print("Awaiting new command...")
    elif command == "PICK":
        print('Recieved command: PICK')
        recieved_heading = clientsocket.recv(4).decode('utf-8').strip()
        recieved_distance = clientsocket.recv(4).decode('utf-8').strip()
        print(recieved_heading)
        clientsocket.close()

        currentHeading = int(recieved_heading)
        print(currentHeading)

        robot.turn_to_heading(currentHeading)

        robot.pickup_ball(recieved_distance)

    elif command == 'DEPO':
        print ('Recieved command: DEPO')

        path_length_in_bytes =  clientsocket.recv(4)

        path_length = int.from_bytes(path_length_in_bytes, 'big')
        path_data = recv_all(clientsocket, path_length).decode('utf-8')
        path_as_dictionaries = json.loads(path_data)

        path = [(d['x'], d['y']) for d in path_as_dictionaries]

        currentX = path[0][0]
        currentY = path[0][1]

        print(currentX, currentY, currentHeading)
        path_length = len(path)
        robot.move_through_path(path[0],path[path_length-1],currentHeading, path, clientsocket)
        robot.deposit()





