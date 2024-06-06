import socket

def establish_socket():
    # Create a socket object
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = "0.0.0.0"
    port = 9999

    # Bind to the port
    serversocket.bind((host, port))

    return socket
