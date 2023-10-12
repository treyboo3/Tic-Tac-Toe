# Name: Trey Booritch
# OSU Email: booritct@oregonstate.edu
# Course: CS372 - Computer Networks
# Due Date: June 6, 2023,
# Description: This script contains the Client class, which is used to establish a connection to a server for sending
# and receiving messages. It is designed to communicate with a corresponding server over a network via sockets.
#
# In addition to sending and receiving messages, the Client class also supports initiating and playing a game of
# Tic-Tac-Toe with the server. It includes the ability to send game moves to the server, process game updates
# from the server, and check for game completion conditions.
#  This code is based on tutorials from the following sources:
# - Real Python's Python Sockets Tutorial: https://realpython.com/python-sockets/
# - Python's Official Socket Programming HOWTO: https://docs.python.org/3.4/howto/sockets.html

import socket
import json
from tictactoe import *


class Client:
    """
        This class implements a client for a tic-tac-toe game.
        It interacts with a server, allowing a game of tic-tac-toe to be played over a network.

        Attributes:
            host (str): The host name/IP address of the server to connect to.
            port (int): The port number of the server to connect to.
            tictactoe (TicTacToe): The current tic-tac-toe game.
            tictactoe_player_server (str): The symbol representing the server player in the game.
            tictactoe_player_client (str): The symbol representing the client player in the game.

        Methods:
            start_client(): Connects to the server and begins the game.
        """

    def __init__(self, host='localhost', port=2000):
        self.host = host
        self.port = port
        self.tictactoe = None  # Store tictactoe object
        self.tictactoe_player_server = None  # Either x or o
        self.tictactoe_player_client = None  # Either x or o

    def start_client(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                # Connect to the server
                client_socket.connect((self.host, self.port))
                messages = [
                    f"Connected to: {self.host} on port: {self.port}",
                    "Type /q to quit",
                    "Enter message to send. Please wait for input prompt before entering message...",
                    "Note: Type 'play tictactoe' to start a game of tictactoe",
                ]
                print("\n".join(messages))

                initial_message = True  # Flag first message has yet to be sent
                game_mode = False  # Flag for game_mode

                while True:
                    # Send initial message
                    if initial_message:
                        client_input = input('Enter Input >')
                        client_socket.sendall(client_input.encode())
                        initial_message = False

                    # Receive response from server and print
                    server_response = client_socket.recv(4096).decode()
                    # If no response from server, then invalid
                    if not server_response:
                        print("Received empty response from server")
                        break
                    # If server decides to quit, also quit
                    if server_response == "/q":
                        print("Server has decided to quit the program.")
                        break  # Break the loop and end the connection

                    # If playing tictactoe, deal with JSON response object and update variables
                    if game_mode:
                        try:
                            response_object = json.loads(server_response)
                            self.tictactoe.board = response_object["board"]
                            self.tictactoe_player_client = response_object["client character"]
                            self.tictactoe_player_server = response_object["server character"]
                            game_status = response_object["game status"]
                            print(self.tictactoe)
                            # Handle game status
                            if game_status != "ongoing":
                                game_mode = False
                                print(game_status)
                        except json.JSONDecodeError:
                            print("Received non-JSON response while in game mode")
                    else:
                        # Display Server Response
                        print(server_response)

                    # If the client initialized the game and server responded with instructions, client starts move
                    if server_response == instructions():
                        game_mode = True
                        self.tictactoe = TicTacToe()  # create store tictactoe object
                        self.tictactoe_player_server = "O"
                        self.tictactoe_player_client = "X"

                    # If playing tictactoe, make a move and send JSON object
                    if game_mode:
                        valid_move = False
                        while not valid_move:
                            client_input = input("Make your move >")
                            if client_input == "/q":
                                print("Client has decided to quit the game.")
                                game_mode = False
                                break
                            valid_move = self.tictactoe.move(int(client_input), self.tictactoe_player_client)
                            if not valid_move:
                                print("Invalid move. Please try again.")

                        print(str(self.tictactoe))

                        game_status = "ongoing"
                        # Check for winner or draw after the client's move
                        if self.tictactoe.check_winner(self.tictactoe_player_client):
                            print("Client won the game!")
                            game_status = "Client won"
                            game_mode = False
                        elif self.tictactoe.check_draw():
                            print("The game is a draw!")
                            game_status = "draw"
                            game_mode = False

                        tictactoe_data = {
                            "server character": self.tictactoe_player_server,
                            "client character": self.tictactoe_player_client,
                            "board": self.tictactoe.board,
                            "game status": game_status
                        }
                        json_tictactoe_data = json.dumps(tictactoe_data)
                        client_socket.sendall(json_tictactoe_data.encode())

                    # Initialize game
                    elif server_response == 'play tictactoe':
                        print("initializing Tic-Tac-Toe from server request")
                        game_mode = True  # Set game_mode flag
                        self.tictactoe = TicTacToe()
                        tictactoe_instructions = instructions()
                        print(tictactoe_instructions)
                        client_socket.sendall(tictactoe_instructions.encode())

                    # Normal Messages
                    else:
                        # Reply to server
                        client_input = input('Enter Input >')
                        if client_input == "/q":
                            print("Client has decided to quit the program.")
                            client_socket.sendall("/q".encode())  # Inform server about termination
                            break  # Break the loop and end the connection
                        client_socket.sendall(client_input.encode())

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    client = Client()
    client.start_client()
