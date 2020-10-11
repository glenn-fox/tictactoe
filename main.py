import random
from os import system


def convert_to_base_3(board):
    # used for quickly storing game states for searching
    # converts board state to base 3 number than to base 10
    total = 0
    for index, value in enumerate(board):
        if value == "X":
            total += 1 * 3**index
        elif value == "O":
            total += 2 * 3**index
    return total


def get_board_from_number(num):
    output = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    i = 8
    while i >= 0:
        while True:
            if num - 3**i >= 0:
                output[i] += 1
                num = num - 3**i
            else:
                break
        i -= 1
    return output


def new_board():
    # returns empty board for cleaner code
    return [" "] * 9


def create_entry(game_board, game_state):
    num_beads = "10 "
    output = "%d " % game_state
    for i in game_board:
        if i == " ":
            output += num_beads
        else:
            output += "0 "
    output += "\n"
    return output


def get_move(game_board):
    # opens the file, checks for the game state in file or creates new entry
    # returns the move index
    possible_moves = {0, 1, 2, 3, 4, 5, 6, 7, 8}
    with open("menace.txt", "r+") as menace:
        file = menace.readlines()
        game_state = convert_to_base_3(game_board)
        not_in_file = True

        # check if game_state is in file return move probabilities
        for item in file:
            item = item.split()
            if str(game_state) == item[0]:
                del item[0]
                move_prob = item
                not_in_file = False

        # if game_state is not in file, make new entry and return the move probabilities
        if not_in_file:
            new_entry = create_entry(game_board, game_state)
            menace.write(new_entry)
            new_entry = new_entry.split()
            del new_entry[0]
            move_prob = new_entry

        for i, j in enumerate(move_prob):
            move_prob[i] = int(j)

        # create weighted list
        weighted_list = []
        for move in possible_moves:
            weighted_list += [move] * move_prob[move]
        return random.choice(weighted_list)


def train(move, winning_player, game_state):
    # stores file into memory
    with open("menace.txt", "r") as memory:
        memory = memory.readlines()
    # deletes file then rewrites it with changes
    with open("menace.txt", "w") as file:
        for line in memory:
            line_list = line.split()
            if line_list[0] == str(game_state):
                if str(winning_player) == "Player":
                    change = int(line_list[move+1])
                    line_list[move+1] = str(change - 1)
                    output = ""
                    for item in line_list:
                        output += item + " "
                    output += "\n"
                    file.write(output)
                    # computer looses
                elif winning_player == "Draw" or winning_player == "Computer":
                    # computer wins or draw
                    change = int(line_list[move + 1])
                    line_list[move + 1] = str(change + 3)
                    output = ""
                    for item in line_list:
                        output += item + " "
                    output += "\n"
                    file.write(output)
            else:
                file.write(line)


class Game:
    def __init__(self):
        # normal games will start with blank board and no winner that will be updated elsewhere in the class
        self.board = new_board()
        self.winner = ""

    def draw(self):
        # draws the board
        system("cls")
        print("\n")
        print(self.board[0] + " | " + self.board[1] + " | " + self.board[2])
        print("--+---+--")
        print(self.board[3] + " | " + self.board[4] + " | " + self.board[5])
        print("--+---+--")
        print(self.board[6] + " | " + self.board[7] + " | " + self.board[8])

    def check_win(self):
        # checks for winning conditions or draw game
        # returns True when winning condition is present or draw
        # top horizontal line
        if self.board[0] != " " and self.board[0] == self.board[1] and self.board[1] == self.board[2]:
            if self.board[0] == "X":
                self.winner = "Computer"
            elif self.board[0] == "O":
                self.winner = "Player"
        # middle horizontal line
        elif self.board[3] != " " and self.board[3] == self.board[4] and self.board[4] == self.board[5]:
            if self.board[3] == "X":
                self.winner = "Computer"
            elif self.board[3] == "O":
                self.winner = "Player"
        # bottom horizontal line
        elif self.board[6] != " " and self.board[6] == self.board[7] and self.board[7] == self.board[8]:
            if self.board[6] == "X":
                self.winner = "Computer"
            elif self.board[6] == "O":
                self.winner = "Player"
        # left vertical line
        elif self.board[0] != " " and self.board[0] == self.board[3] and self.board[3] == self.board[6]:
            if self.board[0] == "X":
                self.winner = "Computer"
            elif self.board[0] == "O":
                self.winner = "Player"
        # middle vertical line
        elif self.board[1] != " " and self.board[1] == self.board[4] and self.board[4] == self.board[7]:
            if self.board[1] == "X":
                self.winner = "Computer"
            elif self.board[1] == "O":
                self.winner = "Player"
        # right vertical line
        elif self.board[2] != " " and self.board[2] == self.board[5] and self.board[5] == self.board[8]:
            if self.board[2] == "X":
                self.winner = "Computer"
            elif self.board[2] == "O":
                self.winner = "Player"
        # diagonals
        elif self.board[0] != " " and self.board[0] == self.board[4] and self.board[4] == self.board[8]:
            if self.board[0] == "X":
                self.winner = "Computer"
            elif self.board[0] == "O":
                self.winner = "Player"
        elif self.board[2] != " " and self.board[2] == self.board[4] and self.board[4] == self.board[6]:
            if self.board[2] == "X":
                self.winner = "Computer"
            elif self.board[2] == "O":
                self.winner = "Player"
        elif " " not in self.board:
            self.winner = "Draw"

        # for printing winner/draw and returning winner to other code
        if self.winner != "":
            self.draw()
            if self.winner == "Draw":
                print("Draw game")
            else:
                print(self.winner + " wins!!")
            return True, self.winner
        return False, self.winner

    def computer_move(self):
        move = get_move(self.board)
        self.board[move] = "X"
        return move

    def player_turn(self):
        while True:
            move = input("Please select a move")
            try:
                move = int(move)
            except ValueError:
                pass
            if move in [1, 2, 3, 4, 5, 6, 7, 8, 9] and self.board[move-1] == " ":
                self.board[int(move)-1] = "O"
                break
            else:
                self.draw()
                print("Invalid move, try again.")

    def start_turn(self):
        # get board state
        board_state = convert_to_base_3(self.board)

        # computer makes move
        last_pc_move = self.computer_move()

        # draw board
        self.draw()

        # check for win
        game_done, winner = self.check_win()
        if game_done:
            train(last_pc_move, self.winner, board_state)
            return winner

        # player makes move
        self.player_turn()

        # check for win
        game_done, winner = self.check_win()
        if game_done:
            train(last_pc_move, self.winner, board_state)
            return winner

        # start next turn if game is not done
        if not game_done:
            self.start_turn()

        # test
        train(last_pc_move, self.winner, board_state)
        # if player win subtract from move
        # else add to move


# main game code

keep_playing = ""
while keep_playing != "n":
    game = Game()
    game.start_turn()
    keep_playing = input("Continue playing? [Y/n]").lower()
