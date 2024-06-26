import pygame,math,random
import PyUI as pyui

from Utility_functions import *
from Entities.Spider.Spider import Spider 

class Player(Spider):
    def __init__(self,ui,x,y,leg_name='Base',body_name='Base',weapon_name='Base'):

        self.team = 'Player'
        self.keybinds = {'UP':[pygame.K_w,pygame.K_UP],
                         'DOWN':[pygame.K_s,pygame.K_DOWN],
                         'LEFT':[pygame.K_a,pygame.K_LEFT],
                         'RIGHT':[pygame.K_d,pygame.K_RIGHT],
                         'SHOOT':[pygame.K_SPACE],
                         'DASH':[pygame.K_SPACE],
                         'RELOAD':[pygame.K_r]}

        self.mpos = (0,0)

        super().__init__(ui,x,y,leg_name,body_name,weapon_name)


    def control(self,mapp,projectiles,entities):
        self.move_vector = pygame.Vector2()
        if self.get_pressed('UP'): self.move_vector[1]-=1 
        if self.get_pressed('DOWN'): self.move_vector[1]+=1
        if self.get_pressed('LEFT'): self.move_vector[0]-=1
        if self.get_pressed('RIGHT'): self.move_vector[0]+=1
        
    
        self.target_body_angle = math.atan2(self.mpos[1]-self.y,self.mpos[0]-self.x)


        if self.get_pressed('SHOOT'):
            self.shoot(projectiles)
        if self.get_pressed('RELOAD'):
            self.reload()
            
    def get_pressed(self,code):
        if code in self.keybinds:
            for k in self.keybinds[code]:
                if self.ui.kprs[k]:
                    return True
        return False

    def render_hud(self,Surf):
        self.weapon.render_hud(Surf)

        
