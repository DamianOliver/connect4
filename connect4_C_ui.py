from ctypes import *
so_file = "./minimax.so"
minimax = CDLL(so_file)

# use command: gcc -shared -o minimax.so -fPIC minimax4.c  to write c file to so file

import pygame as pg
import numpy as np
import random as rand
import timeit

SCREEN_SIZE = (500, 450)
BACKRGOUND_COLOR = (100, 100, 100)
BOARD_COLOR = (100, 100, 250)
PLAYER_1_COLOR = (250, 20, 20)
PLAYER_2_COLOR = (255, 255, 0)

screen = pg.display.set_mode((SCREEN_SIZE), pg.RESIZABLE)

class UI:
    def __init__(self):
        self.offset = (10, 30)
        self.margin = 3
        self.board_size, self.board_location, self.cell_size = self.calc_variables(game.board_dimension)
        self.num_to_color = {-1 : (0, 0, 0), 1 : (255, 255, 255)}
    
    def calc_variables(self, board_dimension):
        board_size = (SCREEN_SIZE[0] - self.offset[0], SCREEN_SIZE[1] - self.offset[1])
        cell_size = ((board_size[0] / 2) / (board_dimension[0] + 1)) - self.margin
        board_location = (cell_size + self.offset[0], cell_size + self.offset[1])

        return board_size, board_location, cell_size

    def draw(self, position):
        self.draw_background()
        self.draw_cells(position)

    def draw_background(self):
        # pg.draw.rect(screen, (BACKRGOUND_COLOR), ((0, 0), SCREEN_SIZE))
        pg.draw.rect(screen, (100, 0, 0), ((0, 0), SCREEN_SIZE))
        pg.draw.rect(screen, (BOARD_COLOR), (self.board_location, (self.board_size[0] + 20, self.board_size[1] + 20)))

    def draw_cells(self, position):
        offset = self.offset[0] + self.cell_size
        cell_margin = self.margin
        cell_size = (self.cell_size + cell_margin) * 2
        for i, row in enumerate(position):
            for k, cell in enumerate(row):     
                location = (offset + self.board_location[0] + cell_size * k, offset + self.board_location[1] + cell_size * i)
                
                if row[k] == 0:
                    color = BACKRGOUND_COLOR
                else:
                    color = self.num_to_color[position[i][k]]
                
                pg.draw.circle(screen, color, location, self.cell_size)

class Player:
    def __init__(self, color, number):
        self.color = color
        self.number = number

class Game:
    def __init__(self, position, player_list, board_dimension):
        self.position = position
        self.player_list = player_list
        self.board_dimension = board_dimension
        self.curr_player = 1
        self.set_up()

    def set_up(self):
        self.position = np.array([[0 for _ in range(self.board_dimension[0])] for _ in range(self.board_dimension[1])], dtype=np.int32)
        # self.position = np.array([[0, 0, 0, 0, 0, 0, 0],
        #                           [0, 0, 0, 0, 0, 0, 0],
        #                           [0, 0, 0, 0, 0, 0, 0],
        #                           [-1, 0, 0, 0, 0, 0, 0],
        #                           [-1, 0, 0, 0, 0, 0, 0],
        #                           [-1, 0, 0, 0, 0, 0, 0]], dtype=np.int32)

    def restart(self):
        self.set_up()

    def convert_position(self):
        flat = self.position.flatten()
        return flat.ctypes.data_as(POINTER(c_int32))

    def place_piece(self, index):
        for i in range(self.position.shape[0] - 1, -1, -1):
            if self.position[i][index] == 0:
                self.position[i][index] = self.curr_player
                return i
        return -1

    def process_placement(self, index):
        height = self.place_piece(index)
        if height == -1:
            print("woops")
            return -1
        self.curr_player *= -1
        result = minimax.check_for_win_py(self.convert_position(), self.position.shape[0], self.position.shape[1], index, height)
        if result != 0:
            print("player {} won".format(result))
            ui.draw(self.position)
            pg.display.update()
            return -2

        ui.draw(self.position)
        pg.display.update()

        start = timeit.default_timer()
        move = self.get_computer_move(7, 100)
        # move = self.get_computer_move(11, 1)
        print("search completed in {}s".format(timeit.default_timer() - start))
        print("move:", move)
        self.place_piece(move)
        ui.draw(self.position)
        pg.display.update()
        self.curr_player *= -1

    def get_computer_move(self, depth, table_size):
        # computer wants height, width -> 0, 1
        print("the curr player is", self.curr_player)
        move = minimax.minimax_py(self.curr_player, self.convert_position(), self.position.shape[0], self.position.shape[1], depth, table_size)
        print("computer move:", move, "\n")
        return move

    def play_computer_move(self):
        move = self.get_computer_move(7, 100)
        print("move:", move)
        self.place_piece(move)
        ui.draw(self.position)
        pg.display.update()
        self.curr_player *= -1

player_1 = Player(1, 1)
player_2 = Player(-1, 2)

game = Game([], [player_1, player_2], (7, 6))
game.set_up()
ui = UI()

player_index = 1

ui.draw(game.position)
pg.display.update()

# pretty bad fix for fundemental problem. Leaving it alone to work on actual code rather than graphics
actual_board_size = game.board_dimension[0] * (ui.cell_size * 2 + ui.margin)

game.play_computer_move() #really janky but like whatever

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

        if event.type == pg.MOUSEBUTTONDOWN:
            location = pg.mouse.get_pos()[0]
            index = (location - ui.board_location[0]) / actual_board_size * game.board_dimension[0]
            index = int(index)
            if index >= 0 and index < game.board_dimension[0]:
                game.process_placement(index)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                game.restart()
                ui.draw(game.position)
                pg.display.update()