import pygame as pg
import board

SCREEN_SIZE = (1440, 1000)
BACKRGOUND_COLOR = (100, 100, 100)
BOARD_COLOR = (100, 100, 250)
PLAYER_1_COLOR = (250, 20, 20)
PLAYER_2_COLOR = (255, 255, 0)

screen = pg.display.set_mode((SCREEN_SIZE), pg.RESIZABLE)

class UI:
    def __init__(self):
        self.cell_size = (130, 130)
        self.board_size, self.board_location = self.calc_variables(game.board_dimension, self.cell_size)
    
    def calc_variables(self, board_dimension, cell_size):
        board_size = (board_dimension[0] * cell_size[0], board_dimension[1] * cell_size[1])
        
        board_location = ((SCREEN_SIZE[0] - board_size[0]) / 2, (SCREEN_SIZE[1] - board_size[1]) / 2)

        return board_size, board_location

    def draw(self, position):
        self.draw_background()
        self.draw_cells(position)

    def draw_background(self):
        pg.draw.rect(screen, (BACKRGOUND_COLOR), ((0, 0), SCREEN_SIZE))
        pg.draw.rect(screen, (BOARD_COLOR), (self.board_location, (self.board_size[0] + 20, self.board_size[1] + 20)))

    def draw_cells(self, position):
        margin = 20
        circle_size = self.cell_size[0] * 0.85 / 2
        for i in range(len(position)):
            location = (i % game.board_dimension[0] * self.cell_size[0], int(i / (game.board_dimension[1] + 1)) * self.cell_size[1])
            # location = (location[0] + self.board_location[0] + margin + circle_size, location[1] + self.board_location[1] + margin + circle_size)
            if position[i] == "empty":
                color = BACKRGOUND_COLOR
            else:
                color = position[i].color
            
            pg.draw.circle(screen, color, location, circle_size)

class Player:
    def __init__(self, color, number):
        self.color = color
        self.number = number

class Game:
    def __init__(self, position, player_list, board_dimension):
        self.position = position
        self.player_list = player_list
        self.board_dimension = board_dimension

    def set_up(self):
        new_position = []
        for i in range(self.board_dimension[0] * self.board_dimension[1]):
            new_position.append("empty")
        
        self.position = new_position

    def set_up_rows(self):
        position = []
        for i in range(self.board_dimension[0]):
            position.append([])

    def place_piece(self, column, player):
        for i in range(self.board_dimension[1]):
            # print((column + self.board_dimension[0] * (self.board_dimension[1] - 1 - i)))
            if self.position[column + self.board_dimension[0] * (self.board_dimension[1] - 1 - i)] == "empty":
                self.position[column + self.board_dimension[0] * (self.board_dimension[1] - 1 - i)] = player
                last_row = i
                return True, last_row

        return False, None

    def restart(self):
        self.set_up()

    # def check_for_win(self, last_piece):
    #     if self.check_column(last_piece[0]) or self.check_row(last_piece[1]):
    #         print("winnnnnnnnner")
    #     print("check")


player_1 = Player((170, 0, 0), 1)
player_2 = Player((170, 170, 0), 2)

game = Game([], [player_1, player_2], (7, 6))
game.set_up()
ui = UI()

player_index = 0

last_row = 1

ui.draw(game.position)
pg.display.update()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                placed, last_row = game.place_piece(0, game.player_list[player_index % len(game.player_list)])
                if placed:
                    print("last row: ", last_row)
                    player_index += 1
                    ui.draw(game.position)
                    game.check_for_win((0, last_row))
                    pg.display.update()
                    print("position: ", game.position)

            elif event.key == pg.K_2:
                placed, last_row = game.place_piece(1, game.player_list[player_index % len(game.player_list)])
                if placed:
                    player_index += 1
                    ui.draw(game.position)
                    game.check_for_win((1, last_row))
                    pg.display.update()

            elif event.key == pg.K_3:
                placed, last_row = game.place_piece(2, game.player_list[player_index % len(game.player_list)])
                if placed:
                    player_index += 1
                    ui.draw(game.position)
                    game.check_for_win((2, last_row))
                    pg.display.update()

            elif event.key == pg.K_4:
                placed, last_row = game.place_piece(3, game.player_list[player_index % len(game.player_list)])
                if placed:
                    player_index += 1
                    ui.draw(game.position)
                    game.check_for_win((3, last_row))
                    pg.display.update()

            elif event.key == pg.K_5:
                placed, last_row = game.place_piece(4, game.player_list[player_index % len(game.player_list)])
                if placed:
                    player_index += 1
                    ui.draw(game.position)
                    game.check_for_win((4, last_row))
                    pg.display.update()

            elif event.key == pg.K_6:
                placed, last_row = game.place_piece(5, game.player_list[player_index % len(game.player_list)])
                if placed:
                    player_index += 1
                    ui.draw(game.position)
                    game.check_for_win((5, last_row))
                    pg.display.update()

            elif event.key == pg.K_7:
                placed, last_row = game.place_piece(6, game.player_list[player_index % len(game.player_list)])
                if placed:
                    player_index += 1
                    ui.draw(game.position)
                    game.check_for_win((6, last_row))
                    pg.display.update()

            # elif event.key == pg.K_8:
            #     placed, last_row = game.place_piece(7, game.player_list[player_index % len(game.player_list)])
            #     if placed:
            #         player_index += 1
            #         ui.draw(game.position)
            #         game.check_for_win((7, last_row))
            #         pg.display.update()

            # elif event.key == pg.K_9:
            #     placed, last_row = game.place_piece(8, game.player_list[player_index % len(game.player_list)])
            #     if placed:
            #         player_index += 1
            #         ui.draw(game.position)
            #         game.check_for_win((8, last_row))
            #         pg.display.update()

            elif event.key == pg.K_r:
                game.restart()
                ui.draw(game.position)
                pg.display.update()
