WINDOW_WIDTH = 1000
WINDOW_HIGHT = 1000

import pygame as pg


pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HIGHT))



while True:
    pg.display.update()
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

pg.quit()