import socket
import threading
import time
import pickle
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class TicTacToe:
    def __init__(self, host, port):
        self.board = [  [" ", " ", " "],
                        [" ", " ", " "],
                        [" ", " ", " "]
                    ]
        self.turn = "O"
        self.you = "X"
        self.opponent = "O"
        self.winner = None
        self.game_over = False
        self.filled_boards = 0
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def handle_connection(self, client):
        while not self.game_over:
            if self.turn == self.you:
                msg = self.board
                msg = pickle.dumps(msg)
                move = input(f"\nNow is your turn ({self.you}).\nEnter a valid integer move (row,column): ")
                if self.is_valid_movement(move.split(",")):
                    client.send(msg)
                    client.send(move.encode("utf-8"))
                    self.apply_movement(move.split(","), self.you)
                    self.turn = self.opponent
            else:
                print("Wait for your opponent's move.\n")
                data = client.recv(1024)
                if not data:
                    break
                else:
                    self.apply_movement(data.decode("utf-8").split(","), self.opponent)
                    self.turn = self.you

    def apply_movement(self, move, player):
        if self.game_over:
            return
        self.filled_boards += 1
        self.board[int(move[0])][int(move[1])] = player
        self.create_current_board()
        if self.is_game_over():
            if self.winner == self.you:
                print("Congratulations! You win!")
                exit()
            else:
                print("Unfortunately! You lose!")
                exit()
        if self.filled_boards == 9:
                print("Tight Game! It\'s a tie!")
                exit()

    def is_valid_movement(self, move):
        if len(move) < 2:
            print("Invalid! Must have 2 arguments!")
            return False
        if move[0] == "" or move[1] == "":
            print("Invalid! Arguments must not be empty!")
            return False
        if not move[0].isdigit() or not move[1].isdigit():
            print("Invalid! Arguments must be an integer!")
            return False
        if int(move[0]) > 2 or int(move[1]) > 2 or int(move[0]) < 0 or int(move[1]) < 0:
            print("Invalid! Allowed move is between 0-2!")
            return False
        if self.board[int(move[0])][int(move[1])] != " ":
            print(f"Invalid! Cell {int(move[0]),int(move[1])} is already filled!")
            return False
        return True

    def is_game_over(self):
        # diagonal left
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0]
            self.game_over = True
            return True
        # diagonal right
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[0][2]
            self.game_over = True
            return True
        # horizontal
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.game_over = True
                return True
        # vertical
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                self.game_over = True
                return True
        return False

    def create_current_board(self):
        print("\n")
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row < 2:
                print("----------")
        print("\n")

with open(os.path.join(BASE_DIR, "serverconf.conf")) as config_file:
        config = dict(line.strip().split("=") for line in config_file)

HOST = config.get("host")
PORT = int(config.get("port"))

tclient = TicTacToe(HOST, PORT)

# Welcome message
message = tclient.socket.recv(1024).decode()
print(message)

# Input room
message = tclient.socket.recv(1024).decode()
print(message)
room = input()
tclient.socket.sendall(room.encode())

# Receive status
status = tclient.socket.recv(1024).decode()

# If selected room is full
while status.split()[0] == "unavailable":
    print("Room is full! Please enter another room:")
    room = input()
    tclient.socket.sendall(room.encode())
    status = tclient.socket.recv(1024).decode()

# If selected room is not full yet
while status.split()[0] == "waiting":
    print("Please wait for another player to join the room.")
    time.sleep(2)
    status = tclient.socket.recv(1024).decode()
    if(status.split()[0] == 'available'):
        status = "available 1"

# First joining room = first turn
if(status.split()[1] == '1'):
    tclient.you = 'O'
    tclient.opponent = 'X'

start_tictactoe = threading.Thread(target=tclient.handle_connection, args=(tclient.socket, )).start()