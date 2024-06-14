import socket

#Creates a socket object, and established a connection to the robot

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.8.111"
port = 9999

client_socket.connect((host, port))

command = 'LEFT'
client_socket.sendall(command.encode('utf-8'))

# Close the connection
client_socket.close()
