SCREEN_SIZE = (1440, 1000)
SQUARE_SIZE = 100
L_SQUARE_COLOR = (195,165,113)
D_SQUARE_COLOR = (137,93,58)
BACKRGOUND_COLOR = (55, 55, 55)

import pygame as pg
screen = pg.display.set_mode((SCREEN_SIZE), pg.RESIZABLE)

def draw():
    draw_board()

def draw_board():
    pg.draw.rect(screen, (BACKRGOUND_COLOR), ((0, 0), SCREEN_SIZE))
    draw_squares()


def draw_squares():
    for i in range(8):
        start_pos = ((SCREEN_SIZE[0] - SQUARE_SIZE * 8) / 2, ((SCREEN_SIZE[1] - SQUARE_SIZE * 8) /2) + SQUARE_SIZE * i)
        draw_rank(start_pos, i%2)


def draw_rank(start_pos, start_color):
    for i in range(8):
        if (start_color + i) % 2 == 0:
            color = L_SQUARE_COLOR
        else:
            color = D_SQUARE_COLOR
        pg.draw.rect(screen, color, ((start_pos[0] + i * SQUARE_SIZE, start_pos[1]), (SQUARE_SIZE, SQUARE_SIZE)))

draw_board()

pg.display.update()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

        if event.type == pg.VIDEORESIZE:
            SCREEN_SIZE = screen.get_size()
            draw()
            pg.display.update()