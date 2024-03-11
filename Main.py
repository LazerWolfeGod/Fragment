import pygame,math,random,sys,os
import PyUI as pyui

pygame.init()
screenw = 1200
screenh = 900
screen = pygame.display.set_mode((screenw, screenh),pygame.RESIZABLE)
from Level import Level
ui = pyui.UI()
done = False
clock = pygame.time.Clock()
ui.styleload_green()


game = Level(ui)
    

while not done:
    for event in ui.loadtickdata():
        if event.type == pygame.QUIT:
            done = True
    game.game_tick(screen)
    
    ui.rendergui(screen)
    pygame.display.flip()
    clock.tick(60)                                               
pygame.quit() 
