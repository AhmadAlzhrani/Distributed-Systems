import socket
import threading
import pickle
import time

# Define the server's IP address and port
IP = '127.0.0.1'
PORT = 55555
ADDR = (IP, PORT)
SIZE = 256
ID_SIZE = 8
FORMAT = "utf-8"
IDlist = []
SESSION_TIME = '30'

# Define a function to handle incoming client connections
def handle_client(client_socket, client_address):
    print(f'New connection from {client_address}')

    client_socket.recv(SIZE).decode(FORMAT)
    print(f'Connection from {client_address} accepted')
    client_socket.send(SESSION_TIME.encode(FORMAT))
    
    ID = client_socket.recv(ID_SIZE).decode(FORMAT)
    IDlist.append((ID))
    print(f'IDs connected: {IDlist[:]}')
    
    # Receive data from the client
    connected = True
    while connected:
        
        dataReceived = client_socket.recv(SIZE).decode(FORMAT)
        
        if dataReceived == 'Quit':
            connected = False
            print(f'Connection from {client_address} closed, msg: {dataReceived}')
        elif dataReceived == 'List':
            client_socket.send(pickle.dumps(IDlist))
        elif dataReceived == 'Alive':
            seconds = time.time()
        
        
        print(f'Received data from {client_address}: {dataReceived}')
        
        # reply to the client
        dataSent = 'Message received'
        client_socket.send(dataSent.encode(FORMAT))
        
    # Close the client socket
    client_socket.close()
    print(f'Connection from {client_address} closed')
    IDlist.remove(ID)


def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(ADDR)

    # Listen for incoming connections
    server_socket.listen()

    # server is now initialized and ready to accept connections
    print(f'Server listening on {IP}/{PORT}')

    # Main loop to accept incoming connections and spawn new threads to handle them
    while True:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()

        # Spawn a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
        print(f'Active connections: {threading.active_count() - 1} \n')
        print(f'Active threads: {threading.enumerate()} \n')

# Run main() if this file is executed directly
if __name__ == '__main__':
    main()
