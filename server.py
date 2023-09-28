import argparse
import sys
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Command line arguments
parser = argparse.ArgumentParser(description='HTTP Web Server')
parser.add_argument('port', type=int, help='Port to listen on')
parser.add_argument('max_clients', type=int, help='Maximum number of clients')
args = parser.parse_args()

# Initialize server variables
serverPort = args.port
max_connections = args.max_clients
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(max_connections)

# Function to handle individual clients
def handle_client(client_socket, client_address):
    try:
        while True:
            request = client_socket.recv(1024).decode()
            if not request:
                print(f"Connection closed by {client_address}")
                break

            print(f"Received request from {client_address}")

            # Parse HTTP GET request
            lines = request.split("\r\n")
            get_line = lines[0].split(" ")
            filename = get_line[1][1:]

            try:
                with open(filename, 'r') as f:
                    filedata = f.read()
                response = 'HTTP/1.1 200 OK\r\n\r\n' + filedata
            except FileNotFoundError:
                response = 'HTTP/1.1 404 Not Found\r\n\r\n'

            client_socket.send(response.encode())
        client_socket.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        client_socket.close()

# Main server loop
if __name__ == "__main__":
    print(f"Server started on port {serverPort}")
    try:
        while True:
            client_socket, client_address = serverSocket.accept()
            print(f"Connection accepted from {client_address}")
            client_thread = Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down")
        serverSocket.close()
        sys.exit(0)
