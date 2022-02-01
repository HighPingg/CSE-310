import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind tge socket to the port
server_address = ('localhost', 10000)
print('connecting to %s port %s' % server_address, file=sys.stderr)
sock.connect(server_address)

try:
    # Send data
    #message = b'BUNGALS GHANTA SEWPAH BOWL!!!'
    message = b'rey.sky@gmail.com'
    
    print('sending "%s"' % message, file=sys.stderr)
    sock.sendall(message)

    # Takes in the parsed result
    print('received', sock.recv(255).decode('UTF-8'), file=sys.stderr)

finally:
    print('closing socket', file=sys.stderr)
    sock.close()

