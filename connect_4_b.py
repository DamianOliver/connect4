from re import I
import pygame as pg
import board as bd

SCREEN_SIZE = (1440, 1000)
BACKRGOUND_COLOR = (100, 100, 100)
BOARD_COLOR = (100, 100, 250)
PLAYER_1_COLOR = (250, 20, 20)
PLAYER_2_COLOR = (255, 255, 0)

num_positions = 0

WIN_NUM = 4

screen = pg.display.set_mode((SCREEN_SIZE), pg.RESIZABLE)

class UI:
    def __init__(self):
        self.cell_size = (130, 130)
        self.board_size, self.board_location = self.calc_variables(game.board_dimension, self.cell_size)
        self.margin = 20
        self.circle_size = self.cell_size[0] * 0.85 / 2

    def calc_variables(self, board_dimension, cell_size):
        board_size = (board_dimension[0] * cell_size[0], board_dimension[1] * cell_size[1])
        
        board_location = ((SCREEN_SIZE[0] - board_size[0]) / 2, (SCREEN_SIZE[1] - board_size[1]) / 2)

        return board_size, board_location

    def draw(self, board):
        self.draw_background()
        self.draw_cells(board)
        pg.display.update()

    def draw_background(self):
        pg.draw.rect(screen, (BACKRGOUND_COLOR), ((0, 0), SCREEN_SIZE))
        pg.draw.rect(screen, (BOARD_COLOR), (self.board_location, (self.board_size[0] + 20, self.board_size[1] + 20)))

    def draw_cells(self, board):
        for x in range(game.board_dimension[0]):
                for y in range(game.board_dimension[1]):
                    location = (x * self.cell_size[0], y * self.cell_size[1])
                    # watch out for the +1
                    location = (location[0] + self.board_location[0] + self.margin + self.circle_size, location[1] + self.board_location[1] + self.margin + self.circle_size)
                    if game.board[x, y] == "e":
                        color = BACKRGOUND_COLOR
                    elif board[x, y] == 0:
                        color = PLAYER_1_COLOR
                    elif board[x, y] == 1:
                        color = PLAYER_2_COLOR
                    else:
                        print("oh no: ", board[x, y])

                    pg.draw.circle(screen, color, location, self.circle_size)

class Player:
    def __init__(self, color, number, ai):
        self.color = color
        self.number = number
        self.ai = ai

class Game:
    def __init__(self, player_list, board_dimension):
        self.player_list = player_list
        self.board_dimension = board_dimension
        self.game_over = False

    def set_up(self):
        board = bd.Board(self.board_dimension)
        self.fill_with_e(board)
        self.board = board

    def fill_with_e(self, board):
        for x in range(game.board_dimension[0]):
            for y in range(game.board_dimension[1]):
                board[x, y] = "e"

    def place_piece(self, column, player):
        for i in range(self.board_dimension[1]):
            if self.board[column, self.board_dimension[1] - i - 1] == "e":
                self.board[column, self.board_dimension[1] - i - 1] = player
                return True, self.board_dimension[1] - i - 1

        return False, None

    def check_for_win(self, last_piece):
        if self.check_rows(last_piece) == 0 or\
        self.check_columns(last_piece) == 0 or\
        self.check_upr_diagonal(last_piece) == 0 or\
        self.check_upl_diagonal(last_piece) == 0:
            self.handle_end(0)

        if self.check_rows(last_piece) == 1 or\
        self.check_columns(last_piece) == 1 or\
        self.check_upr_diagonal(last_piece) == 1 or\
        self.check_upl_diagonal(last_piece) == 1:
            self.handle_end(1)

    def check_for_draw(self, last_piece):
        if last_piece[1] != 0:
            return False
        for i in range(self.board_dimension[0]):
            if self.board[i, 0] == "e":
                return False
        return True
        
    def check_rows(self, last_piece):
        start_cell = (0, last_piece[1])
        direction = (1, 0)
        cell_list = list(self.board.iterline(start_cell, direction))
        count_0, count_1 = self.check_cells(cell_list)
        if count_0 >= WIN_NUM:
            return 0
        elif count_1 >= WIN_NUM:
            return 1
        else:
            return "none"

    def check_columns(self, last_piece):
        start_cell = (last_piece[0], 0)
        direction = [0, 1]
        cell_list = list(self.board.iterline(start_cell, direction))
        count_0, count_1 = self.check_cells(cell_list)
        if count_0 >= WIN_NUM:
            return 0
        elif count_1 >= WIN_NUM:
            return 1
        else:
            return "none"

    def check_upr_diagonal(self, last_piece):
        start_cell = last_piece
        find_list = list(self.board.iterline(start_cell, (-1, +1)))
        start_cell = find_list[len(find_list) - 1]
        direction = (1, -1)
        cell_list = list(self.board.iterline(start_cell, direction))
        count_0, count_1 = self.check_cells(cell_list)
        if count_0 >= WIN_NUM:
            return 0
        elif count_1 >= WIN_NUM:
            return 1
        else:
            return "none"

    def check_upl_diagonal(self, last_piece):
        start_cell = last_piece
        find_list = list(self.board.iterline(start_cell, (+1, +1)))
        start_cell = find_list[len(find_list) - 1]
        direction = (-1, -1)
        cell_list = list(self.board.iterline(start_cell, direction))
        count_0, count_1 = self.check_cells(cell_list)
        if count_0 >= WIN_NUM:
            return 0
        elif count_1 >= WIN_NUM:
            return 1
        else:
            return "none"

    def check_cells(self, cell_list):
        count_0 = 0
        count_1 = 0
        greatest_count_0 = 0
        greatest_count_1 = 0

        for cell in cell_list:
            # print("counts: ", greatest_count_0, greatest_count_1)
            if self.board[cell[0], cell[1]] == "e":
                if count_0 > greatest_count_0:
                    greatest_count_0 = count_0
                if count_1 > greatest_count_1:
                    greatest_count_1 = count_1
                count_0 = 0
                count_1 = 0
            elif self.board[cell[0], cell[1]] == 0:
                if count_1 > greatest_count_1:
                    greatest_count_1 = count_1
                count_0 += 1
                count_1 = 0
            elif self.board[cell[0], cell[1]] == 1:
                if count_0 > greatest_count_0:
                    greatest_count_0 = count_0
                count_0 = 0
                count_1 += 1
            else:
                print("what the?", self.board[cell[0], cell[1]])

        if count_0 > greatest_count_0:
                    greatest_count_0 = count_0
        if count_1 > greatest_count_1:
            greatest_count_1 = count_1

        return greatest_count_0, greatest_count_1

    def handle_end(self, winner_index):
        self.game_over = True
        if winner_index == "draw":
            print("Game drawn. Good game.")
        elif winner_index == 0:
            print("Human wins. I think the wifi cut out.")
        elif winner_index == 1:
            print("Bot wins. You fought hard.")


class AI():
    def __init__(self, terminal_depth):
        self.terminal_depth = terminal_depth
        self.positions = 0

    def calc_move(self, board):
        num_positions = 0
        best_eval = -10000000
        best_move = None
        for i in range(game.board_dimension[0]):
            print(i, "moves searched")
            placed, last_row = game.place_piece(i, 1)
            if placed:
                eval = self.minimax(False, (i, last_row), board, 1, -10000000, 10000000)
                self.undo((i, last_row))
                print("eval: ", i, eval)
                if eval > best_eval:
                    best_eval = eval
                    best_move = i

        print(best_eval)
        print(num_positions)
        return best_move

    def minimax(self, ai_turn, last_piece, board, depth, alpha, beta):
        if self.calc_if_win(last_piece, board) == "win":
            if ai_turn:
                return -999 * (self.terminal_depth + 1 - depth)
            else:
                return 999 * (self.terminal_depth + 1 - depth)
        if game.check_for_draw(last_piece):
            return 0

        evals = []
        # print(depth)
        if ai_turn:
            player = 1
        else:
            player = 0
        for i in range(game.board_dimension[0]):
            placed, last_row = game.place_piece(i, player)
            if placed:
                # ui.draw(game.board)
                # pg.display.update()
                # pg.time.wait(400)
                if ai_turn:
                    turn = False
                else:
                    turn = True

                if depth == self.terminal_depth:
                    self.undo((i, last_row))
                    evals.append(self.evaluate(board))
                else:
                    evals.append(self.minimax(turn, (i, last_row), board, depth + 1, alpha, beta))
                    self.undo((i, last_row))

                if ai_turn:
                    if max(evals) >= beta:
                        return (max(evals))

                    if max(evals) > alpha:
                        alpha = max(evals)

                else:
                    if min(evals) <= alpha:
                        return (min(evals))

                    if min(evals) < beta:
                        beta = min(evals)

        if ai_turn:
            # print("depth + eval", depth, max(evals))
            return max(evals)
        else:
            # print("depth + eval", depth, max(evals))
            return min(evals)

    def undo(self, last_piece):
        game.board[last_piece] = "e"

    def calc_if_win(self, last_piece, board):
        if game.check_rows(last_piece) == 0 or\
        game.check_columns(last_piece) == 0 or\
        game.check_upr_diagonal(last_piece) == 0 or\
        game.check_upl_diagonal(last_piece) == 0:
            return "win"

        if game.check_rows(last_piece) == 1 or\
        game.check_columns(last_piece) == 1 or\
        game.check_upr_diagonal(last_piece) == 1 or\
        game.check_upl_diagonal(last_piece) == 1:
            return "win"

    def count_num_in_row(self, cell_list, board):
        counts = []

        count_0 = 0
        count_1 = 0
        p_count_0 = 0
        p_count_1 = 0

        for cell in cell_list:
            if board[cell] == "e":
                p_count_0 += 1
                p_count_1 += 1
            elif board[cell] == 0:
                if count_1 + p_count_1 >= WIN_NUM:
                    counts.append((1, count_1))
                count_1 = 0
                p_count_1 = 0
                count_0 += 1
            elif board[cell] == 1:
                if count_0 + p_count_0 >= WIN_NUM:
                    counts.append((0, count_0))
                    count_0 = 0
                    p_count_0 = 0
                    count_1 += 1

        counts.append((0, count_0))
        counts.append((1, count_1))
        return counts

    def evaluate(self, board):
        self.num_positions += 1
        all_counts = []
        score_0 = 0
        score_1 = 0
        for i in range(game.board_dimension[0]):
            start = (i, 0)
            cell_list = list(board.iterline(start, (0, 1)))
            counts = self.count_num_in_row(cell_list, board)
            all_counts.extend(counts)
        for i in range(game.board_dimension[1]):
            start = (0, i)
            cell_list = list(board.iterline(start, (1, 0)))
            counts = self.count_num_in_row(cell_list, board)
            all_counts.extend(counts)

        for count in counts:
            score = 0
            if count[1] == 1:
                score = 1
            elif count[1] == 2:
                score = 3
            elif count[1] == 3:
                score = 9
            if count[0] == 0:
                score_0 += score
            elif count[0] == 1:
                score_1 += score

        # print("evaluated as", score_1 - score_0)
        center_score = self.check_center(board)

        return score_1 - score_0 + center_score

    def check_center(self, board):
        score_0 = 0
        score_1 = 0
        center_dimension = (int(game.board_dimension[0]/2), int(game.board_dimension[1] / 2))
        center_location = ((game.board_dimension[0] - center_dimension[0])/2, game.board_dimension[1] - center_dimension[1])
        for y in range(center_dimension[1]):
            for x in range(center_dimension[0]):
                cell = (int(x + center_location[0]), int(y + center_location[1]))
                if board[cell] == 0:
                    score_0 += 1
                elif board[cell] == 1:
                    score_1 += 1

        return score_1 - score_0




player_1 = Player((170, 0, 0), 1, False)
player_2 = Player((170, 170, 0), 2, True)
game = Game([player_2, player_1], (7, 6))
game.set_up()
ui = UI()
ai = AI(6)

player_index = 0

ui.draw(game.board)
pg.display.update()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

        if not game.player_list[player_index % len(game.player_list)].ai:
            if event.type == pg.MOUSEBUTTONDOWN:
                if not game.game_over:
                    if pg.mouse.get_pos()[0] > ui.board_location[0] and pg.mouse.get_pos()[0] < ui.board_location[0] + ui.margin * 0.5 + ui.circle_size * 2 + ui.margin:
                        placed, last_row = game.place_piece(0, 0)
                        if placed:
                            player_index += 1
                            ui.draw(game.board)
                            game.check_for_win((0, last_row))
                            if game.check_for_draw((0, last_row)):
                                game.handle_end("draw")
                            pg.display.update()
                    elif pg.mouse.get_pos()[0] > ui.board_location[0] + ui.margin * 0.5 + ui.circle_size * 2 + ui.margin and pg.mouse.get_pos()[0] < ui.board_location[0] + ui.margin * 0.5 + (ui.circle_size * 2 + ui.margin) * 2:
                        placed, last_row = game.place_piece(1, 0)
                        if placed:
                            player_index += 1
                            ui.draw(game.board)
                            game.check_for_win((1, last_row))
                            if game.check_for_draw((1, last_row)):
                                game.handle_end("draw")
                            pg.display.update()
                    elif pg.mouse.get_pos()[0] > ui.board_location[0] + ui.margin * 0.5 + (ui.circle_size * 2 + ui.margin) * 2 and pg.mouse.get_pos()[0] < ui.board_location[0] + ui.margin * 0.5 + (ui.circle_size * 2 + ui.margin) * 3:
                        placed, last_row = game.place_piece(2, 0)
                        if placed:
                            player_index += 1
                            ui.draw(game.board)
                            game.check_for_win((2, last_row))
                            if game.check_for_draw((2, last_row)):
                                game.handle_end("draw")
                            pg.display.update()
                    elif pg.mouse.get_pos()[0] > ui.board_location[0] + ui.margin * 0.5 + (ui.circle_size * 2 + ui.margin) * 3 and pg.mouse.get_pos()[0] < ui.board_location[0] + ui.margin * 0.5 + (ui.circle_size * 2 + ui.margin) * 4:
                        placed, last_row = game.place_piece(3, 0)
                        if placed:
                            player_index += 1
                            ui.draw(game.board)
                            game.check_for_win((3, last_row))
                            if game.check_for_draw((3, last_row)):
                                game.handle_end("draw")
                            pg.display.update()
                    elif pg.mouse.get_pos()[0] > ui.board_location[0] + ui.margin * 0.5 + (ui.circle_size * 2 + ui.margin) * 4 and pg.mouse.get_pos()[0] < ui.board_location[0] + ui.margin * 0.5 + (ui.circle_size * 2 + ui.margin) * 5:
                        placed, last_row = game.place_piece(4, 0)
                        if placed:
                            player_index += 1
                            ui.draw(game.board)
                            game.check_for_win((4, last_row))
                            if game.check_for_draw((4, last_row)):
                                game.handle_end("draw")
                            pg.display.update()
                    elif pg.mouse.get_pos()[0] > ui.board_location[0] + ui.margin * 0.5 + (ui.circle_size * 2 + ui.margin) * 5 and pg.mouse.get_pos()[0] < ui.board_location[0] + ui.margin * 0.5 + (ui.circle_size * 2 + ui.margin) * 6:
                        placed, last_row = game.place_piece(5, 0)
                        if placed:
                            player_index += 1
                            ui.draw(game.board)
                            game.check_for_win((5, last_row))
                            if game.check_for_draw((5, last_row)):
                                game.handle_end("draw")
                            pg.display.update()
                    elif pg.mouse.get_pos()[0] > ui.board_location[0] + ui.margin * 0.5 + (ui.circle_size * 2 + ui.margin) * 6 and pg.mouse.get_pos()[0] < ui.board_location[0] + ui.margin * 0.5 + (ui.circle_size * 2 + ui.margin) * 7:
                        placed, last_row = game.place_piece(6, 0)
                        if placed:
                            player_index += 1
                            ui.draw(game.board)
                            game.check_for_win((6, last_row))
                            if game.check_for_draw((6, last_row)):
                                game.handle_end("draw")
                            pg.display.update()

        else:
            if not game.game_over:
                print("doing stuff")
                move = ai.calc_move(game.board)
                placed, last_row = game.place_piece(move, 1)
                player_index += 1
                ui.draw(game.board)
                game.check_for_win((move, last_row))
                if game.check_for_draw((move, last_row)):
                    game.handle_end("draw")
                pg.display.update()
