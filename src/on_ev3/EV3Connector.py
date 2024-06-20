import socket

def establish_socket():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(True)
    # Get local machine name
    host = "0.0.0.0"
    port = 9999

    # Bind to the port
    s.bind((host, port))
    s.listen(5)

    return s
