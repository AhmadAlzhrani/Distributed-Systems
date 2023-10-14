import socket
import threading
import time


# Define the server's IP address and port
IP = '127.0.0.1'
PORT = 55555
ADDR = (IP, PORT)
SIZE = 256
FORMAT = "utf-8"
IDlist = []
SESSION_TIME = '20'
finish_thread = False

# Define a function to handle commands sending
def send():
    global finish_thread

    # the command prompt loop
    while finish_thread == False:
            
        dataReceived = input("> ")
        print('\n')
        if dataReceived == '@Quit':
            # Send data to the server as Quit command
            client_socket.send(dataReceived[1:].encode(FORMAT))
            print(f'Session Closed')
            finish_thread = True
            
        elif dataReceived == '@List':
            # Send data to the server as List command
            client_socket.send(dataReceived[1:].encode(FORMAT))
        
        elif dataReceived.startswith('('):
            
            # Send message to another client through the server
            index = dataReceived.find(')')
            destinationID = dataReceived[1:index]
            print(f'destinationID:{destinationID}')
            
            msg = dataReceived[index+2:]
            print(f'message:{msg}')
            
            # padding the destination IDs
            if len(destinationID.encode(FORMAT)) < 8:
                destinationID = destinationID.ljust(8, ' ')
                print("less")
                
                # checking the message length
                if len(msg.encode(FORMAT)) < 240:
                    print(destinationID+msg+ID+'0')
                    client_socket.send((destinationID+msg+ID+'0').encode(FORMAT))
                    print(f'Sent data to server: {dataReceived}')
                else:
                    print("Message is too long")
                    
            elif len(destinationID.encode(FORMAT)) > 8:
                print("Wrong destination ID")
            
# Define a function to handle receiving data
def receive():
    global finish_thread

    while finish_thread == False:
        
        # Receive messages from the server
        recvData= client_socket.recv(SIZE).decode(FORMAT)
        print(f'[SERVER] {recvData}')

# Define a function to handle sending alive signal
def alive():
    seconds = time.time()
    global finish_thread

    while finish_thread == False:
        
        # checking the session time
        if time.time() - seconds > int(SESSION_TIME):
            print('Refreshing connection')
            client_socket.send('Alive'.encode(FORMAT))
            seconds = time.time()
        else:
            pass


# Run main if this file is executed directly
if __name__ == '__main__':
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(ADDR)
    print(f'Trying to connect to the server at {IP}/{PORT}')

    # Send connection signal and receive session time
    client_socket.send('Connect'.encode(FORMAT))
    print("CONNECTED")
    
    timeInterval = client_socket.recv(SIZE).decode(FORMAT)
    print(f'the time interval for this connection to be active is {timeInterval} seconds')

    # ID validation
    ID = input("Enter your ID: ")
    if len(ID.encode(FORMAT)) < 8:
        ID = ID.ljust(8, ' ')
    elif len(ID.encode(FORMAT)) > 8:
        ID = ID[:8]
    
    # send ID to the server
    client_socket.send(ID.encode(FORMAT))
    client_socket.send('Alive'.encode(FORMAT))

    # Create separate threads to send and receive data and the alive signal
    thread_send = threading.Thread(target = send)
    thread_send.start()

    thread_receive = threading.Thread(target = receive)
    thread_receive.start()  
    
    thread_alive = threading.Thread(target = alive)
    thread_alive.start()