import pygame as pg
import random as rd
#from animals import 


pg.init()

n= 10
L= 50
screen = pg.display.set_mode((L*n,L*n))
clock = pg.time.Clock()
running = True 

R = 0
while running and  R< MAX_TURNS:

    clock.tick(1)
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                running = False


    rect = pg.Rect(n,n, L,L)
    color = (255, 0, 0)
    pg.draw.rect(screen, color, rect)
    
    pg.display.update()

