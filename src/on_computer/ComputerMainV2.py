import socket
from RobotController import RobotController

HOST = "192.168.8.111"
PORT = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

controller = RobotController(client_socket)


