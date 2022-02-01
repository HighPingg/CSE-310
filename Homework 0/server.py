import socket
import sys

def interpretMessage(message):
    if b'@' in message and b'.' in message:
        name = message.split(b'@')[0].split(b'.')
        return name[0].capitalize() + b' ' + name[1].capitalize()
    else:
        return message

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind tge socket to the port
server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection', file=sys.stderr)
    connection, client_address = sock.accept()

    try:
        print('connection from', client_address, file=sys.stderr)

        data = connection.recv(255)
        print('received %s' % data, file=sys.stderr)
        
        # We now want to parse the data and wait for the result
        message = interpretMessage(data)
        print('sending %s' % message, file=sys.stderr)
        connection.sendall(message)
        
    finally:
       # Clean up the connection
       connection.close()
