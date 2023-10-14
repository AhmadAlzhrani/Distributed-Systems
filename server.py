import socket
import threading
import time

# Define the server's IP address and port
IP = '127.0.0.1'
PORT = 55555
ADDR = (IP, PORT)
SIZE = 256
ID_SIZE = 8
FORMAT = "utf-8"
IDlist = []
SOClist = []
ACTIVE = []
SESSION_TIME = '30'

def All():
    for user in SOClist:
        user.send(('updated list:'+(str(IDlist))).encode(FORMAT))
        print('Update sent')
        
def timer():
    seconds = time.time()
    while True:
        if time.time() - seconds > int(SESSION_TIME):
            print(f'{SESSION_TIME} seconds passed')
            inactive = set(IDlist) - set(ACTIVE)
            inactive = list(inactive)
            print(f'Inactive users: {inactive}')
            for user in inactive:
                indexInactive=IDlist.index(user)
                SOCinactive = SOClist[indexInactive]
                SOCinactive.close()
            seconds = time.time()
        else:
            pass


# Define a function to handle incoming client connections
def Rec(client_socket, client_address):
    print(f'New connection from {client_address}')

    client_socket.recv(SIZE).decode(FORMAT)
    print(f'Connection from {client_address} accepted')
    client_socket.send(SESSION_TIME.encode(FORMAT))
    
    ID = client_socket.recv(ID_SIZE).decode(FORMAT)
    ID = ID.rstrip()
    IDlist.append(ID)
    SOClist.append(client_socket)
    print(f'IDs connected: {IDlist[:]}')
    print(f'Sockets connected: {SOClist[:]}')
    All()
    
    # Receive data from the client
    connected = True
    while connected:
        try:
            dataReceived = client_socket.recv(SIZE).decode(FORMAT)
        except:
            IDlist.remove(ID.rstrip())
            SOClist.remove(client_socket)
            print(f'user {ID} is inactive thus disconnected')
            All()
            return
        
        if dataReceived == 'Quit':
            connected = False
            print(f'Connection from {client_address} closed, msg: {dataReceived}')
            All()
        elif dataReceived == 'List':
            client_socket.send((str(IDlist)).encode(FORMAT))
        elif dataReceived == 'Alive':
            # do some thread shit cast or somthin
            ACTIVE.append(ID)
        else:
            sourceID = dataReceived[-9:-2]
            sourceID = sourceID.rstrip()
            destinationID = dataReceived[0:7]
            destinationID = destinationID.rstrip()
            message = dataReceived[8:-9]
            
            # search in arrays for ID and send message to that ID
            if destinationID in IDlist:
                index = IDlist.index(destinationID)
                SOClist[index].send(('message from: '+sourceID+'\n'+ message).encode(FORMAT))
                print(f'Message sent to {destinationID} from {sourceID}')
                print(f'Message is: {message}')
            else:
                print(IDlist)
                index = IDlist.index(sourceID)
                SOClist[index].send((f'{destinationID} is not online').encode(FORMAT))
            
        
        print(f'Received data from {client_address}: {dataReceived}')
        
        # reply to the client
        dataSent = 'Message reached the server'
        client_socket.send(dataSent.encode(FORMAT))
        
    # Close the client socket
    client_socket.close()
    IDlist.remove(ID.rstrip())
    SOClist.remove(client_socket)


def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(ADDR)

    # Listen for incoming connections
    server_socket.listen()

    # server is now initialized and ready to accept connections
    print(f'Server listening on {IP}/{PORT}')
    
    timer_thread = threading.Thread(target=timer)
    timer_thread.start()
    
    # Main loop to accept incoming connections and spawn new threads to handle them
    while True:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()

        # Spawn a new thread to handle the client connection
        client_thread = threading.Thread(target=Rec, args=(client_socket, client_address))
        client_thread.start()
        print(f'Active connections: {threading.active_count() - 1} \n')
        print(f'Active threads: {threading.enumerate()} \n')

# Run main() if this file is executed directly
if __name__ == '__main__':
    main()
