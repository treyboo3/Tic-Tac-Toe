# Name: Trey Booritch
# OSU Email: booritct@oregonstate.edu
# Course: CS372 - Computer Networks
# Due Date: June 6, 2023,
# Description: This script contains the Server class, which is used to establish a server that listens for incoming
# connections from clients. It is designed to communicate with a corresponding client over a network via sockets.
#
# In addition to sending and receiving messages, the Server class also supports initiating and playing a game of
# Tic-Tac-Toe with the client. It includes the ability to receive game moves from the client, process these moves,
# and send game updates to the client, including checking for game completion conditions.
#   This code is based on tutorials from the following sources:
# - Real Python's Python Sockets Tutorial: https://realpython.com/python-sockets/
# - Python's Official Socket Programming HOWTO: https://docs.python.org/3.4/howto/sockets.html

import socket
import json
from tictactoe import TicTacToe, instructions


class Server:
    """
     This class implements a server for a tic-tac-toe game.
     It interacts with a client, allowing a game of tic-tac-toe to be played over a network.

     Attributes:
         host (str): The host name/IP address on which the server is running.
         port (int): The port number on which the server is listening.
         tictactoe (TicTacToe): The current tic-tac-toe game.
         tictactoe_player_server (str): The symbol representing the server player in the game.
         tictactoe_player_client (str): The symbol representing the client player in the game.

     Methods:
         start_server(): Starts the server and begins listening for connections.
     """

    def __init__(self, host='localhost', port=2000):
        self.host = host
        self.port = port
        self.tictactoe = None  # Store tictactoe object
        self.tictactoe_player_server = None  # Either x or o
        self.tictactoe_player_client = None  # Either x or o

    def start_server(self):
        try:
            running = True
            # Create a socket with default values for PYTHON SOCKET API
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((self.host, self.port))
                server_socket.listen(1)
                print(f"Server is listening on: {self.host} on port: {self.port}")

                while running:
                    # Accept connections from client
                    connection_socket, client_address = server_socket.accept()
                    with connection_socket:
                        messages = [
                            f"Connected by {client_address}",
                            "Wait for message from client and input prompt before entering message... ",
                            "Type /q to quit"
                        ]
                        print("\n".join(messages))

                        game_mode = False  # Flag for game mode

                        while True:
                            # Receive response from client and print
                            client_response = connection_socket.recv(1024).decode()
                            # If no response from client, then invalid
                            if not client_response:
                                print("Received empty response from client")
                                break
                            # If client decides to quit, also quit
                            if client_response == "/q":
                                print("Client has decided to quit the program.")
                                running = False
                                break  # Break the loop and end the connection

                            # If playing tictactoe, deal with JSON response object and update variables
                            if game_mode:
                                try:
                                    response_object = json.loads(client_response)
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
                                # Display Client Response
                                print(client_response)

                            # If the server initialized the game and client responded with instructions,
                            # server starts move
                            if client_response == instructions():
                                game_mode = True
                                self.tictactoe = TicTacToe()  # create store tictactoe object
                                self.tictactoe_player_server = "X"
                                self.tictactoe_player_client = "O"

                            # If playing tictactoe, make a move and send JSON object
                            if game_mode:
                                valid_move = False
                                while not valid_move:
                                    server_input = input("Make your move >")
                                    if server_input == "/q":
                                        print("Server has decided to quit the game.")
                                        game_mode = False
                                        break
                                    valid_move = self.tictactoe.move(int(server_input), self.tictactoe_player_server)
                                    if not valid_move:
                                        print("Invalid move. Please try again.")

                                print(str(self.tictactoe))

                                game_status = "ongoing"
                                # Check for winner or draw after the server's move
                                if self.tictactoe.check_winner(self.tictactoe_player_server):
                                    print("Server won the game!")
                                    game_status = "Server won"
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
                                connection_socket.sendall(json_tictactoe_data.encode())

                            # Initialize game
                            elif client_response == 'play tictactoe':
                                print("initializing Tic-Tac-Toe from client request")
                                game_mode = True  # Set game_mode flag
                                self.tictactoe = TicTacToe()
                                tictactoe_instructions = instructions()
                                print(tictactoe_instructions)
                                connection_socket.sendall(tictactoe_instructions.encode())

                            # Normal Messages
                            else:
                                # Reply to client
                                server_input = input('Enter Input >')
                                if server_input == "/q":
                                    print("Server has decided to quit the program.")
                                    connection_socket.sendall("/q".encode())  # Inform client about termination
                                    running = False
                                    break  # Break the loop and end the connection
                                connection_socket.sendall(server_input.encode())

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    server = Server()
    server.start_server()
