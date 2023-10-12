# Name: Trey Booritch
# OSU Email: booritct@oregonstate.edu
# Course: CS372 - Computer Networks
# Due Date: June 6, 2023,
# Description: This script contains the TicTacToe class, which is used to model a game of Tic Tac Toe. It maintains the
# game board and supports making moves by either player, as well as checking for a winning condition or a draw.
#
# Each game is represented as a TicTacToe instance with an internal game board. A player's move is made by calling
# the move() method with the index of the desired board position and the player's character (either 'X' or 'O').
#
# The game board can be checked for a winning condition using the check_winner() method, or for a draw using
# the check_draw() method. The current state of the game board can also be output as a string using the __str__() method


def instructions():
    list_of_instructions = """Game has started! You can make a move by entering the index of the square you want to move to.    

The board is structured as follows with corresponding index:    
                        0 | 1 | 2
                        ---------
                        3 | 4 | 5
                        ---------
                        6 | 7 | 8   
For example, if you want to mark the center square, you would type '4'.
    """
    return list_of_instructions


class TicTacToe:
    """
        This class represents a Tic-Tac-Toe game.

        Attributes:
            board (list): A list representing the game board. Empty cells are represented by ' '.

        Methods:
            move(index: int, player: str) -> bool: Makes a move on the game board.
            check_winner(player: str) -> bool: Checks if a player has won the game.
            check_draw() -> bool: Checks if the game is a draw.
            __str__() -> str: Returns a string representation of the game board.
    """
    def __init__(self):
        """Initializes the TicTacToe class with an empty game board."""
        self.board = [' ' for _ in range(9)]  # Start with empty board

    def move(self, index, player):
        """
        Makes a move on the game board.

        Parameters:
            index (int): The index of the cell to place the move in.
            player (str): The player making the move.

        Returns:
            bool: True if the move was valid, False otherwise.
        """
        # If spot is empty
        if self.board[index] == ' ':
            self.board[index] = player  # Make the move
            return True     # Valid move
        return False    # Invalid move

    def check_winner(self, player):
        """
        Checks if a player has won the game.

        Parameters:
            player (str): The player to check for a win.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]

        for combination in winning_combinations:
            if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] == player:
                return True

        return False

    def check_draw(self):
        """
        Checks if the game is a draw.

        Returns:
            bool: True if the game is a draw, False otherwise.
        """
        return all(cell != ' ' for cell in self.board)

    def __str__(self):
        """
        Returns a string representation of the game board.

        Returns:
            str: The game board as a string.
        """
        return '\n'.join([
            ' | '.join(self.board[i:i + 3]) + '\n' + '-' * 9
            for i in range(0, 9, 3)
        ])[:-9]  # Remove the last "---"

