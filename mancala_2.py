from copy import deepcopy
import sys

# sys.setrecursionlimit(10000)

board = [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], [0, 0]]
# board = [[1, 1, 1, 1, 0, 1, 1, 99, 0, 0, 0, 0], [0, 200]]
# board = [[1, 0, 2, 7, 7, 0, 6, 6, 7, 7, 0, 0], [0, 0]]
# 3  | 5  | 0  | 0  | 2  | 1  | 8  | 3
#    | 8  | 8  | 10 | 0  | 0  | 0  |
# board = [[5, 0, 0, 2, 1, 8, 0, 0, 0, 10, 8, 8], [3, 3]]
# # 4  | 0  | 2  | 1  | 0  | 2  | 11 | 5
# #    | 1  | 1  | 1  | 11 | 9  | 0  |
# board = [[0, 2, 1, 0, 2, 11, 1, 1, 1, 11, 9, 0], [4, 5]]

def draw(board):
    print("     0    1    2    3    4    5")
    print("{:<2} | {:<2} | {:<2} | {:<2} | {:<2} | {:<2} | {:<2} | {:<2}".format(board[1][0], board[0][0], board[0][1], board[0][2], board[0][3], board[0][4], board[0][5], board[1][1]))
    # print("   ------------------------------")
    print("   | {:<2} | {:<2} | {:<2} | {:<2} | {:<2} | {:<2} |".format(board[0][11], board[0][10], board[0][9], board[0][8], board[0][7], board[0][6]))
    print("     5    4    3    2    1    0")
    print()
    print()
 
def move(board, index, dcopy):
    if dcopy:
        move_board = [x.copy() for x in board] 
    else:
        move_board = board
    num_pieces = move_board[0][index]
    move_board[0][index] = 0
    if index <= 5:
        current_side = 1
        num_in_points = int((index + num_pieces + 6) / 12)
        move_board[1][1] += num_in_points
        num_pieces -= num_in_points
    else:
        current_side = -1
        num_in_points = int((index + num_pieces) / 12)
        move_board[1][0] += num_in_points
        num_pieces -= num_in_points

    for i in range(num_pieces):
        move_board[0][(i + index + 1) % len(move_board[0])] += 1

    last_index = (num_pieces + index) % len(move_board[0])

    if move_board[0][last_index] == 1:
        if last_index == 5 or last_index == 11:
            if num_in_points > 0:
                return move_board
        if last_index <= 5 and current_side == 1:
            if not dcopy:
                if move_board[0][11 - last_index] > 2:
                    print("-------------------")
                    print("I hate you program. You lost {} points.".format(move_board[0][11 - last_index]))
                    print("-------------------")
            move_board[1][1] += move_board[0][11 - last_index]
            move_board[0][11 - last_index] = 0
        if last_index >= 6 and current_side == -1:
            move_board[1][0] += move_board[0][11 - last_index]
            move_board[0][11 - last_index] = 0

    return move_board

def check_go_again(index, board):
    if index <= 5:
        if board[0][index] + index == 6:
            return True
    else:
        if index > len(board[0]):
            print("uh oh:", index)
        if board[0][index] + index == 12:
            return True

    return False

def check_game_over(board):
    a = True
    b = True
    for i in range(0, 5):
        if board[0][i] != 0:
            a = False
    for i in range(6, 12):
        if board[0][i] != 0:
            b = False
    if a or b:
        return True
    return False


def play():
    current_player = 1
    while True:
        if check_game_over(board):
            print("Game Over.")
            exit()
        draw(board)
        if current_player == -1:
            go_again = ai_2.play_move(board, -1)
            # go_again = Player().play_move(board, 1)
        else:
            go_again = Player().play_move(board, 1)
            # go_again = ai.play_move(board, 1)
        if not go_again:
            current_player *= -1
        else:
            print("go again")

class Player():
    def play_move(self, board, player_index):
        while True:
            index = int(input("Enter Index: "))
            if player_index == -1:
                index += 6
            if board[0][index] != 0:
                go_again = check_go_again(index, board)
                move(board, index, False)
                return go_again

        

class AI():
    def __init__(self, max_depth, index):
        self.max_depth = max_depth
        self.index = index
        self.positions = 0
        self.end_positions = 0

    def calculate(self, depth, current_index, calc_board, alpha, beta):
        if depth >= self.max_depth:
            if board[1][1] + board[1][0] > 24:
                top_total = board[0][0] + board[0][1] + board[0][2] + board[0][3] + board[0][4] + board[0][5]
                bottom_total = board[0][11] + board[0][10] + board[0][9] + board[0][8] + board[0][7] + board[0][6]
                return (((board[1][1] + board[1][0]) / 96) * 1) * (top_total - bottom_total)
            self.positions += 1
            return calc_board[1][1] - calc_board[1][0]

        evals = []
        blanks = 0

        if current_index == 1:
            index_offset = 0
        else:
            index_offset = 6

        for i in range(6):
            if calc_board[0][i + index_offset] != 0:
                if check_go_again(i, calc_board):
                    # print("calc go again")
                    index_mult = 1
                else:
                    index_mult = -1
                test_board = move(calc_board, i + index_offset, True)
                # print("test board", i, "depth:", depth)
                # draw(test_board)
                evals.append(self.calculate(depth + 1, current_index * index_mult, test_board, alpha, beta))
            else:
                blanks += 1
                if current_index == 1:
                    evals.append(-1000)
                else:
                    evals.append(1000)
            if current_index == 1:
                if max(evals) >= beta:
                    return (max(evals))

                if max(evals) > alpha:
                    alpha = max(evals)

            else:
                if min(evals) <= alpha:
                    return (min(evals))

                if min(evals) < beta:
                    beta = min(evals)

        if blanks == 6:
            # print("reached end with score:", (calc_board[1][1] + board[0][0] + board[0][1] + board[0][2] + board[0][3] + board[0][4] + board[0][5]) - (calc_board[1][0] + board[0][11] + board[0][10] + board[0][9] + board[0][8] + board[0][7] + board[0][6]))
            self.end_positions += 1
            return (calc_board[1][1] + board[0][0] + board[0][1] + board[0][2] + board[0][3] + board[0][4] + board[0][5]) - (calc_board[1][0] + board[0][11] + board[0][10] + board[0][9] + board[0][8] + board[0][7] + board[0][6])

        if current_index == 1:
            best_eval = -10000
            best_move = None

            for i in range(len(evals)):
                if evals[i] > best_eval:
                    best_eval = evals[i]
                    best_move = i

        elif current_index == -1:
            best_eval = 10000
            best_move = None

            for i in range(len(evals)):
                if evals[i] < best_eval:
                    best_eval = evals[i]
                    best_move = i

        if depth == 1:
            if len(evals) > len(board[0]):
                print("what the:", evals, board[0])
            if blanks >= 6:
                print("Game Over. Prepare for error")
                return "gg"
            print("evals:", evals)
            return best_move

        return best_eval

    def simple_eval(board):
        return board[1][1] - board[1][0]

    def advanced_eval(board):
        top_total = board[0][0] + board[0][1] + board[0][2] + board[0][3] + board[0][4] + board[0][5]
        bottom_total = board[0][11] + board[0][10] + board[0][9] + board[0][8] + board[0][7] + board[0][6]



    def play_move(self, board, player_index):
        self.positions = 0
        self.end_positions = 0
        index = self.calculate(1, player_index, board, -10000, 10000)
        if index == 16:
            print("why is it 16?")
        # index = self.calculate(1, 1, board)
        if player_index == -1:
            index += 6
        go_again = check_go_again(index, board)
        move(board, index, False)
        if player_index == 1:
            print("AI Index of", self.index, "->", index)
        else:
            print("AI Index of", self.index, "->", index - 6)
        print("positions not at end:", self.positions)
        print("end positions:", self.end_positions)
        return go_again

print("running")
ai = AI(11, 1)
ai_2 = AI(11, -1)
player_list = [Player(), ai]

play()