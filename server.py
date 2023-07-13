import socket
import threading
import os
import time
import pickle

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class TServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))

    def handle_client(self, client_socket, client_id):
        # Welcome Message
        welcome = "Welcome to Tic Tac Toe, Player {}".format(client_id+1)
        client_socket.send(welcome.encode())
        
        # Prompt to choose room
        clients[client_id].sendall('Choose room : '.encode())
        roomId = clients[client_id].recv(1024).decode()

        # Initialize room with roomId
        if roomId not in roomFull:
            roomFull[roomId] = []

        # Check if room is full
        while len(roomFull[roomId]) >= 2:
            clients[client_id].sendall(("unavailable " + str(len(roomFull[roomId]))).encode())
            roomId = client_socket.recv(1024).decode()

            if roomId not in roomFull:
                roomFull[roomId] = []
        
        roomFull[roomId].append(client_id)
        
        # Check if room is not full yet -> ask client to wait
        while len(roomFull[roomId]) < 2:
            clients[client_id].sendall(("waiting " + str(len(roomFull[roomId]))).encode())
            time.sleep(2)
            roomFull[roomId] = roomFull[roomId]
        
        clients[client_id].sendall(("available " + str(len(roomFull[roomId]))).encode())
        
        while True:
            try:
                gamestate = client_socket.recv(1024)
                if not gamestate:
                    roomFull[roomId] = []
                    break
                gamestate = pickle.loads(gamestate) 
                print("Board from Player {}: {}".format(client_id+1, gamestate))

                message = client_socket.recv(1024).decode()
                if not message:
                    roomFull[roomId] = []
                    break
                print("Received from client {}: {}".format(client_id+1, message))

                # Send the received message to the other client
                if(client_id == roomFull[roomId][0]):
                    other_client_id = roomFull[roomId][1]
                else:
                    other_client_id = roomFull[roomId][0]

                clients[other_client_id].sendall(message.encode())

            except:
                break

        client_socket.close()
        print("Client {} disconnected".format(client_id+1))

    def start_server(self):
        self.socket.listen(6)

        print('Server started. Listening on port 8000...')
        id = 0

        while True:
            client_socket, client_address = self.socket.accept()
            print(f'New client connected: {client_address[0]}:{client_address[1]}')

            # Assign an ID to the client
            client_id = id
            id = id + 1
            clients[client_id] = client_socket

            # Start a new thread to handle the client
            threading.Thread(target=self.handle_client, args=(client_socket, client_id, )).start()

roomFull = {}
clients = {}

with open(os.path.join(BASE_DIR, "serverconf.conf")) as config_file:
        config = dict(line.strip().split("=") for line in config_file)

HOST = config.get("host")
PORT = int(config.get("port"))

tserver = TServer(HOST, PORT)
tserver.start_server()