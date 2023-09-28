import argparse
from socket import socket, AF_INET, SOCK_STREAM

# Command line arguments
parser = argparse.ArgumentParser(description='HTTP Web Client')
parser.add_argument('port', type=int, help='Port to connect to')
parser.add_argument('filename', type=str, help='File name to request')
args = parser.parse_args()

# Initialize client variables
serverIP = '127.0.0.1'
serverPort = args.port
filename = args.filename
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

# Send HTTP GET request and receive response
get_request = f"GET /{filename} HTTP/1.1\r\nHost: {serverIP}\r\n\r\n"
clientSocket.send(get_request.encode())
response = clientSocket.recv(1024).decode()

# Parse and save the file if it exists
lines = response.split("\r\n\r\n")
header = lines[0]
filedata = lines[1]
if "200 OK" in header:
    with open(f"received_{filename}", 'w') as f:
        f.write(filedata)
else:
    print("Received 404 Not Found")

clientSocket.close()
