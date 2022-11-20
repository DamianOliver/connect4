board = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
point_sections = [0, 0]
board_length = 6

def move(index, board):
    num_pieces = board[index]
    board[index] = 0
    num_added = 0
    if index <= 5:
        if point_sections[1] + board[index] >= 7:

    for i in range(num_pieces):
        board[(index + i + 1) % (len(board) - 1)] += 1

    return board
        
def draw(board):
    print(point_sections[0], "|", board[0], "|", board[1], "|", board[2], "|", board[3], "|",  board[4], "|", board[5], "|", point_sections[1])
    print("  |", board[6], "|", board[7], "|", board[8], "|", board[9], "|", board[10], "|", board[11], "|")
    print()
    print()
    
draw(board)
move(4, board)
draw(board)

# def can_go_again(board, index):
#     if index + board[index] == 7


class AI:
    def __init__(self, index, max_depth):
        self.index = index
        self.max_depth = max_depth

    def calculate(self, current_index, depth, board):
        evals = []
        if depth == self.max_depth:
            return board[0] - board[7]

        if current_index == self.index:
            for i in range(1, board_length + 1):
                test_board = move(i, board)
                evals.append(self.calculate(current_index * -1, depth + 1, test_board))
            best_eval = -10000
            best_move = None
            for i in range(len(evals)):
                if evals[i] > best_eval:
                    best_eval = evals[i]
                    best_move = i
        else:
            for i in range(7, board_length + 6):
                test_board = move(i, board)
                evals.append(self.calculate(current_index * -1, depth + 1, test_board))

            best_eval = 10000
            best_move = None

            for i in range(len(evals)):
                if evals[i] < best_eval:
                    best_eval = evals[i]
                    best_move = i

        return best_move

ai = AI(1, 5)

print(ai.calculate(1, 0, board))


    # def find_move(self, board):
    #     if self.index == 1:
    #         best_move = None
    #         best_eval = -10000
    #         evals = []
    #         for i in range(6):
    #             test_board = move(board, i, True)
    #             evals.append(self.calculate(1, -1, test_board))
    #             print(i, evals[i])

    #         for i in range(len(evals)):
    #             if evals[i] > best_eval:
    #                 best_eval = evals[i]
    #                 best_move = i

    #     else:
    #         best_move = None
    #         best_eval = 10000
    #         evals = []
    #         for i in range(6):
    #             test_board = move(board, i, True)
    #             evals.append(self.calculate(1, -1, test_board))
    #             print(i, evals[i])

    #         print("evals:", evals)

    #         for i in range(len(evals)):
    #             if evals[i] < best_eval:
    #                 best_eval = eval
    #                 best_move = i

    #     print("best:", best_move)
    #     return best_move
