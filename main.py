# Trying to create a command-line version of minesweeper with python
import random
import re


class Board:
    def __init__(self, height, width, bombs):
        self.height = height
        self.width = width
        self.bombs = bombs

        self.board = self.create_empty_board()
        self.plant_bombs()
        self.find_bomb_adjacent_values()

        self.dug = set()  # keep track of which locations are uncovered

    def show_covered_board(self):
        # create an array that represents what the user would see
        visible_board = [[None for _ in range(self.width)]
                         for _ in range(self.height)]
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = '-'

        # turn that array into a string
        col_labels_1 = '  | '
        for col in range(self.width):  # label the columns
            if col + 1 < 10:
                col_labels_1 += ('  ')
            elif col + 1 > 9:
                col_labels_1 += (str((col + 1) // 10) + ' ')
        print(col_labels_1)
        col_labels_2 = '  | '
        for col in range(self.width):  # label the columns
            if col + 1 < 10:
                col_labels_2 += (str(col + 1) + ' ')
            elif col + 1 > 9:
                col_labels_2 += (str((col + 1) % 10) + ' ')
        print(col_labels_2)

        col_underscores = '__|_'
        for col in range(self.width):  # put underscores under it to seperate the labels from the board
            col_underscores += ("__")
        print(col_underscores)

        # print the rows proceeded by a label and pipeline symbol
        for row in range(self.height):
            if row + 1 < 10:
                row_str = str(row + 1) + ' | '
            else:
                row_str = str(row + 1) + '| '
            for col in range(self.width):
                row_str += (str(visible_board[row][col]) + ' ')
            print(row_str)

    def create_empty_board(self):
        # make a board based on height, width, and number of bombs
        board = [[None for _ in range(self.width)]
                 for _ in range(self.height)]  # create empty board
        return board

    def plant_bombs(self):
        board = self.board
        bombs_needed = self.bombs
        while bombs_needed > 0:
            location = random.randint(0, (self.width * self.height) - 1)
            # find the row and column where the bomb has been planted
            row = location // self.width
            col = location % self.width
            # print(location, row, col)

            if board[row][col] == '*':
                # bomb is already here
                continue

            board[row][col] = '*'  # plant bomb in this spot
            bombs_needed -= 1

        # print(board)
        return board

    def find_bomb_adjacent_values(self):
        # assign a value 0-8 for all non-bomb spaces
        # the value represents the number of bombs adjacent to the space
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == '*':
                    # this spot IS a bomb itself, so we continue
                    continue

                adjacent_bomb_count = 0
                for r in range(max(0, row - 1), min(self.height - 1, (row + 1)) + 1):
                    for c in range(max(0, col - 1), min(self.width - 1, (col + 1)) + 1):
                        if r == row and c == col:
                            # this is the location we're currently checking
                            continue
                        if self.board[r][c] == '*':
                            adjacent_bomb_count += 1

                self.board[row][col] = adjacent_bomb_count

    def dig(self, row, col):
        # return False if digging a bomb, return True if else
        # dig bomb= game over
        # dig at location with adjacent bombs
        # dig at location with no adjacent bombs -> uncover all adjacent spots with no adjacent bombs
        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False  # game over
        elif self.board[row][col] > 0:
            return True

        # if we get here we've uncovered a 0 spot
        for r in range(max(0, row - 1), min(self.height - 1, (row + 1)) + 1):
            for c in range(max(0, col - 1), min(self.width - 1, (col + 1)) + 1):
                if (r, c) in self.dug:
                    continue  # we've already dug here
                self.dig(r, c)

        return True


def play(difficulty):
    # Create board and plant bombs
    if difficulty == "easy":
        board = Board(8, 8, 10)
    elif difficulty == "medium":
        board = Board(16, 16, 40)
    elif difficulty == "hard":
        board = Board(16, 30, 99)
        board.dig(7, 2)
        board.show_covered_board()

    # Ask user where to dig

    # If location is bomb, game over
    # If not a bomb, dig recursively until every uncovered square is next to a
    #   bomb
    # Repeat until game over
    safe = True

    while len(board.dug) < (board.width * board.height) - board.bombs:
        board.show_covered_board()
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))
        row, col = int(user_input[0]) - 1, int(user_input[-1]) - 1
        if row < 0 or row >= board.height or col < 0 or col >= board.width:
            print("Invalid location. Try again.")
            continue

        safe = board.dig(row, col)
        if not safe:
            # dug up a bomb
            break

    if safe:
        print("CONGRATULATIONS! YOU WIN!")
    else:
        print("Sorry, you hit a bomb! Game over.")
        board.dug = [(r, c) for r in range(board.height) for c in range(board.width)]
        board.show_covered_board()
    print()


print("Hello! Welcome to command line Minesweeper!")
keep_playing = True
while keep_playing:
    user_difficulty = input("Would you like to play on easy, medium, or hard difficulty? \n")
    user_difficulty = user_difficulty.lower()
    if user_difficulty == "easy" or user_difficulty == "medium" or user_difficulty == "hard":
        play(user_difficulty)
    else:
        print("Invalid difficulty. Please enter your input as: easy, medium, or hard.")
        continue
    while True:
        user_continue = input("Would you like to play again? Y or N: ")
        user_continue = user_continue.lower()
        if user_continue == "y":
            keep_playing = True
            break
        elif user_continue == "n":
            keep_playing = False
            break
        else:
            "Invalid input, please enter Y or N."
            continue
