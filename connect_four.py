
# Name: Fares Elbermawy
# Description: implementation of a program that simulates the game connect 4. There are two options in this game.
# You either play against a real person or against the pc which choses the play based on random numbers.

import random
from abc import ABC, abstractmethod
import math

# Specifying the number of rows and columns.
rows_number = 6
columns_number = 5


# The class which let the user chose between game modes and maybe change it later in different games.
class Game:
    def __init__(self):
        self._game_mode = None

    def choose_mode(self, user_input):
        if user_input == 'Q':
            exit()
        elif user_input == 'H':
            self._game_mode = Human()
        elif user_input == "A":
            self._game_mode = Random()
        elif user_input == "I":
            self._game_mode = AI()
        else:
            print("Wrong input! Try again")
            return False
        return True

    def game_run(self):
        self._game_mode.game_run()


# The parent class which represents the game mode.
class GameMode(ABC):
    def __init__(self):
        self._player_number = 1

    @abstractmethod
    # The abstract method which defines how the game will work. It is implemented in each game mode accordingly.
    def game_run(self):
        raise NotImplementedError

    # This is to check if the character is to quit or restart.
    def check_character(self, user_input):
        if user_input == 'Q':
            exit()
        elif user_input == 'R':
            return True


# Naming classes according to the type of the opponent
class Human(GameMode):
    def __init__(self):
        super().__init__()

    def game_run(self):
        # Keep the method running until the user asks to quit or restart or the situation changes
        while True:
            print_board()
            column_of_play = input(f"player {self._player_number} plays!, select column(0-{columns_number - 1}),  press Q to quit, R to restart")
            # Check if the character is R then it returns and restarts the game.
            if self.check_character(column_of_play):
                return
            column_of_play = int(column_of_play)
            # Updating the board with the input of user and returning the row value
            row_of_play = update_cell(board, column_of_play, self._player_number, False)
            # Making the function to return a specific letter if something was wrong with the input. Then it asks for a valid input until a valid one is there.
            while row_of_play == 'E':
                column_of_play = input(f"player {self._player_number} plays!, select column(0-{columns_number - 1}), press Q to quit, R to restart")
                column_of_play = int(column_of_play)
                row_of_play = update_cell(board, column_of_play, self._player_number, False)
            if situation_change(board, row_of_play, column_of_play, self._player_number):
                return
            elif self._player_number == 1:
                self._player_number = 2
            else:
                self._player_number = 1


class Random(GameMode):
    def __init__(self):
        super().__init__()

    def game_run(self):
        while True:
            if self._player_number == 1:
                print_board()
                column_of_play = input(f"player {self._player_number} plays!, select column(0-{columns_number - 1}),  press Q to quit, R to restart")
                if self.check_character(column_of_play):
                    return
            else:
                column_of_play = random.randint(0, 3)
            column_of_play = int(column_of_play)
            row_of_play = update_cell(board, column_of_play, self._player_number, False)
            # Checking if the random number is valid.
            while row_of_play == 'E':
                if self._player_number == 2:
                    column_of_play = random.randint(0, 3)
                else:
                    column_of_play = input(f"player {self._player_number} plays!, select column(0-{columns_number - 1}), press Q to quit, R to restart")
                column_of_play = int(column_of_play)
                row_of_play = update_cell(board, column_of_play, self._player_number, False)
            if situation_change(board, row_of_play, column_of_play, self._player_number):
                return
            self._player_number = 2 if self._player_number == 1 else 1

class AI(GameMode):
    def __init__(self):
        self._player_number = 1
        self._AI_number = 2
        self._turn = self._player_number

    def game_run(self):
        while True:
            if self._turn == 1:
                print_board()
                column_of_play = input(f"player {self._player_number} plays!, select column(0-{columns_number - 1}),  press Q to quit, R to restart")
                if self.check_character(column_of_play):
                    return
            else:
                column_of_play, minimax_score = self.minimax(board, 5, -math.inf, math.inf, True)
            column_of_play = int(column_of_play)
            row_of_play = update_cell(board, column_of_play, self._turn, False)
            # Checking if the number is valid.
            while row_of_play == 'E':
                if self._turn == 2:
                    column_of_play = random.randint(0, 3)
                else:
                    column_of_play = input(f"player {self._player_number} plays!, select column(0-{columns_number - 1}), press Q to quit, R to restart")
                column_of_play = int(column_of_play)
                row_of_play = update_cell(board, column_of_play, self._turn, False)
            if situation_change(board, row_of_play, column_of_play, self._turn):
                return
            self._turn = 2 if self._turn == 1 else 1

    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(columns_number-3):
            for r in range(rows_number):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(columns_number):
            for r in range(rows_number-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(columns_number-3):
            for r in range(rows_number-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(columns_number-3):
            for r in range(3, rows_number):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

    def is_terminal_node(self, board_input):
        return self.winning_move(board_input, self._player_number) or self.winning_move(board, self._AI_number) or len(self.get_valid_locations(board)) == 0

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(columns_number):
            clone_board = board.copy()
            if update_cell(clone_board, col, self._AI_number, True) != 'E':
                valid_locations.append(col)
        return valid_locations

    def score_position(self, board_input, piece):
        score = 0
        # Score center column
        center_array = [int(i) for i in list(board_input[:, columns_number//2])]
        center_count = center_array.count(piece)
        score += center_count * 3
        # Score Horizontal
        for r in range(rows_number):
            row_array = [int(i) for i in list(board_input[r, :])]
            for c in range(columns_number-3):
                window = row_array[c:c+4]  # 4 is the number of pieces to win
                score += evaluate_window(window, piece)
        # Score Vertical
        for c in range(columns_number):
            col_array = [int(i) for i in list(board_input[:, c])]
            for r in range(rows_number-3):
                window = col_array[r:r+4]
                score += evaluate_window(window, piece)
        # Score posiive sloped diagonal
        for r in range(rows_number-3):
            for c in range(columns_number-3):
                window = [board_input[r+i][c+i] for i in range(4)]
                score += evaluate_window(window, piece)

        for r in range(rows_number-3):
            for c in range(columns_number-3):
                window = [board_input[r+3-i][c+i] for i in range(4)]
                score += evaluate_window(window, piece)

        return score

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self._player_number
        if piece == self._player_number:
            opp_piece = self._AI_number

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, self._AI_number):
                    return (None, 100000000000000)
                elif self.winning_move(board, self._player_number):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.score_position(board, self._AI_number))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = board.copy()
                row = update_cell(b_copy, col, self._AI_number, True)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = board.copy()
                row = update_cell(b_copy, col, self._AI_number, True)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value


# Function to print the board
def print_board():
    for row in board:
        for cell in row:
            print(f'| {cell} ', end='')
        print('|')
        print('-' * (4 * columns_number + 1))


# Function to update a cell with a specific value
def update_cell(board_input,column, player, AI):
    if column >= columns_number or board_input[0][column] != '*':
        if not AI:
            print("Error! Cannot put the element in this column. Try again")
        return 'E'
    for row in range(rows_number - 1, -1, -1):
        if board_input[row][column] == '*':
            board_input[row][column] = player
            return row


# A function which checks if the situation changed. Either by winning of the player or the board is full and a draw happened.
def situation_change(board_input, row_element, column_element, player):
    if row_win(board_input, row_element, column_element, player) or diagonal_win(board_input, row_element, column_element, player) or column_win(board_input, row_element, player):
        print_board()
        print(f"Player {player} wins!")
        return True
    elif draw():
        print_board()
        print("The game ended with a draw!")
        return True
    else:
        return False


# Checking if the board is full.
def draw():
    for column in range(0, columns_number):
        if board[0][column] == '*':
            return False
    return True


# Checking if the player won horizontally.
def column_win(board_input, row_element, player):
    for possibility in range(0, columns_number - 3):
        consecutive_elements = 0
        for column_index in range(possibility, possibility + 4):
            if board_input[row_element][column_index] == player:
                consecutive_elements += 1
        if consecutive_elements == 4:
            return True
    return False


# Checking of winning vertically.
def row_win(board_input, row_element, column_element, player):
    if row_element + 3 >= rows_number:
        return False
    for i in range(row_element, row_element + 4):
        if board_input[i][column_element] != player:
            return False
    return True


# Checking of winning diagonally.
def diagonal_win(board_input, row_element, column_element, player):
    col = column_element
    row = row_element
    if row_element >= rows_number // 2:
        return False
    # The diagonal goes to the right i.e: increase in column and row number
    elif column_element < columns_number // 2:
        col += 1
        row += 1
        for i in range(0, 3):
            if board_input[row][col] != player:
                return False
            col += 1
            row += 1
        return True
    # The diagonal goes to the left i.e: increase in row and decrease in column number
    elif column_element > columns_number // 2:
        row += 1
        col -= 1
        for i in range(0, 3):
            if board_input[row][col] != player:
                return False
            row += 1
            col -= 1
        return True
    else:
        return False


# The main function. Keeps running until quit.
while True:
    # Initialize the board with '*'
    board = [['*' for _ in range(columns_number)] for _ in range(rows_number)]
    choose_game = Game()
    user_requirement = input("Welcome to the game! Press H to play against another human, A to play against random, I to play against AI, Q to quit!")
    if not choose_game.choose_mode(user_requirement):
        continue
    choose_game.game_run()
