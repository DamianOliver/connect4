import random as rand

def simulate(num_filled, pre_filled):
    board = set_up_board(num_filled, pre_filled)

    if check_row(board):
        return True

    if check_column(board):
        return True

    if check_diagonal(board):
        return True

    return False


def set_up_board(num_filled, prefilled):
    board = []
    for i in range(25 - len(prefilled)):
        board.append(0)
    for i in range(num_filled - len(prefilled)):
        board[i] = 1

    rand.shuffle(board)

    # print("pre  insert", board)

    for i in range(len(prefilled)):
        board.insert(prefilled[i], 1)

    # print("post insert", board)

    return board

def check_row(board):
    for i in range(0, 25, 5):
        if board[int(i)] == 1:
            if board[int(i+1)] == 1:
                if board[int(i+2)] == 1:
                    if board[int(i+3)] == 1:
                        if board[int(i+4)] == 1:
                            # print(board)
                            return True

def check_column(board):
    for i in range(5):
        if board[int(i)] == 1:
            if board[int(i+5)] == 1:
                if board[int(i+10)] == 1:
                    if board[int(i+15)] == 1:
                        if board[int(i+20)] == 1:
                            # print(board)
                            return True

def check_diagonal(board):
    if board[0] == 1:
        if board[6] == 1:
            if board[12] == 1:
                if board[18] == 1:
                    if board[24] == 1:
                        # print(board)
                        return True
    if board[4] == 1:
        if board[8] == 1:
            if board[12] == 1:
                if board[16] == 1:
                    if board[20] == 1:
                        # print(board)
                        return True



num_win = 0
total = 10000
print("running")

for i in range(total):
    if simulate(10, []):
        num_win += 1

print("win percent =", num_win / total * 100,"%", "total wins:", num_win)

# empty is 0.02297%
# center is 0.037040000000000003%
# edge is 0.01844%
# 0 and 1 is 0.0558899 and 12 13 is 0.05666
# 0 1 2 is 0.43185999999999997%
# 0 1 2 3 is 4.7536000000000005%
# 0 1 3 4 is 100.0%

# empty fill 6 is 0.13455%
# center fill 5 is 0.2%
# center fill 6 is 0.68269%

# checked at 1000000
# empty fill 10 is 5.6366
# empty fill 11 is 

# empty fill 20 is 99.9%
# empty fill 21 is 100.0%


