import socket
import threading

# Define the server's IP address and port
HOST = '127.0.0.1'
PORT = 55555
SIZE = 256
FORMAT = "utf-8"

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

# Define a function to handle incoming client connections
def handle_client(client_socket, client_address):
    print(f'New connection from {client_address}')

    # Receive data from the client
    connected = True
    while connected:
        dataReceived = client_socket.recv(SIZE).decode(FORMAT)
        if dataReceived == 'Quit':
            connected = False
        print(f'Received data from {client_address}: {dataReceived.decode()}')
        
        # reply to the client
        dataSent = f'Received data: {dataReceived}'
        client_socket.send(dataSent.encode(FORMAT))
        
    # Close the client socket
    client_socket.close()
    print(f'Connection from {client_address} closed, msg: {dataReceived}')

# Main loop to accept incoming connections and spawn new threads to handle them
while True:
    # Accept a new client connection
    client_socket, client_address = server_socket.accept()

    # Spawn a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()