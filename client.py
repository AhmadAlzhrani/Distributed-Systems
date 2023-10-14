import socket
import pickle
import time

# Define the server's IP address and port
IP = '127.0.0.1'
PORT = 55555
ADDR = (IP, PORT)
SIZE = 256
FORMAT = "utf-8"
IDlist = []
SESSION_TIME = 20


def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(ADDR)
    print(f'Trying to connect to the server at {IP}/{PORT}')

    client_socket.send('Connect'.encode(FORMAT))
    print("CONNECTED")
    
    timeInterval = client_socket.recv(SIZE)
    print(f'the time interval for this connection to be active is {timeInterval} seconds')
    
    ID = input("Enter your ID: ")
    client_socket.send(ID.encode(FORMAT))
    

    connected = True
    while connected:
            
        dataReceived = input("> ")
        
        if dataReceived == '@Quit':
            # Send data to the server as Quit command
            client_socket.send(dataReceived[1:].encode(FORMAT))
            print(f'Session Closed')
            connected = False
            
        elif dataReceived == '@List':
            # Send data to the server as Quit command
            client_socket.send(dataReceived[1:].encode(FORMAT))
            IDlist = pickle.loads(client_socket.recv(SIZE))
            print('Current list of online clients: \n',IDlist)
        
        else:
            # Send data to the server
            client_socket.send(dataReceived.encode(FORMAT))
            print(f'Sent data to server: {dataReceived}')
            # Receive data from the server
            dataSent = client_socket.recv(SIZE).decode(FORMAT)
            print(f'Received data from server: {dataSent}')

# Run main() if this file is executed directly
if __name__ == '__main__':
    main()  