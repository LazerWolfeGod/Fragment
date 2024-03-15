import pygame,math,random,sys,os
import PyUI as pyui

pygame.init()
screenw = 1200
screenh = 900
screen = pygame.display.set_mode((screenw, screenh),pygame.RESIZABLE)
ui = pyui.UI()
done = False
clock = pygame.time.Clock()
ui.styleload_green()

from Level import Level


game = Level(ui)
    

while not done:
    for event in ui.loadtickdata():
        if event.type == pygame.QUIT:
            done = True
    game.game_tick(screen)
    
    ui.rendergui(screen)
    ui.write(screen,1,1,str(round(clock.get_fps(),1)),20,center=False)
    pygame.display.flip()
    clock.tick(60)                                               
pygame.quit() 
