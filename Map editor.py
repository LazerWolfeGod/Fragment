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

from Environment.Map import *
from Camera import Camera
from Player import Player

class Editor(Player):
    def render_surf(self):
        surf = pygame.Surface((1,1))
        surf.set_alpha()
        return surf
    def edit(self,camera,tilemap):
        pos = camera.screen_pos_to_world_pos(ui.mpos)
        grid_pos = tilemap.world_pos_to_grid_pos(pos)
        




mapp = Map(128)
editor = Editor(ui,0,0)
camera = Camera(editor,pygame.Rect(10,10,1180,880))


while not done:
    for event in ui.loadtickdata():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(pyui.Style.wallpapercol)
    camera.move()
    camera.render(screen,mapp,[editor],[],[])
    editor.edit(mapp.tilemap)
    editor.control(0,[])

    
    
    ui.rendergui(screen)
    ui.write(screen,1,1,str(round(clock.get_fps(),1)),20,center=False)
    pygame.display.flip()
    clock.tick(60)                                               
pygame.quit() 
