import pygame,math,random
import PyUI as pyui

from Utility_functions import *
from Spider.Spider import Spider 

class Player(Spider):
    def __init__(self,ui,x,y):
        self.ui = ui
        self.x = x
        self.y = y
        self.velocity = pygame.Vector2()
        self.angular_velocity = 0
        self.angle = 0
        self.target_angle = 0
        
        self.keybinds = {'UP':[pygame.K_w,pygame.K_UP],
                         'DOWN':[pygame.K_s,pygame.K_DOWN],
                         'LEFT':[pygame.K_a,pygame.K_LEFT],
                         'RIGHT':[pygame.K_d,pygame.K_RIGHT],
                         'SHOOT':[pygame.K_SPACE],
                         'DASH':[pygame.K_SPACE]}

        self.mpos = (0,0)

        super().__init__('Green','Green','Flamer')


    def control(self,tilemap,projectiles):
        delta_vel = pygame.Vector2()
        if self.get_pressed('UP'): delta_vel[1]-=1 
        if self.get_pressed('DOWN'): delta_vel[1]+=1
        if self.get_pressed('LEFT'): delta_vel[0]-=1
        if self.get_pressed('RIGHT'): delta_vel[0]+=1
        if delta_vel.magnitude()>0: delta_vel.normalize_ip()
        delta_vel*=(5+math.cos(self.angle-delta_vel.as_polar()[1]/180*math.pi))/6
        delta_vel*=self.move_acceleration*self.ui.deltatime
        
        self.velocity+=delta_vel
        

        self.target_angle = math.atan2(self.mpos[1]-self.y,self.mpos[0]-self.x)
        if (self.angle-self.target_angle)%math.tau<(self.target_angle-self.angle)%math.tau:
            self.angular_velocity-=min(self.turn_acceleration,(self.angle-self.target_angle)%math.tau)
        else:
            self.angular_velocity+=min(self.turn_acceleration,(self.target_angle-self.angle)%math.tau)

        self.angular_velocity*=0.3
        self.angle+=self.angular_velocity

        self.velocity[0]*=self.move_friction**self.ui.deltatime
        self.velocity[1]*=self.move_friction**self.ui.deltatime

        prev_x = self.x
        self.x+=self.velocity[0]*self.ui.deltatime
        if self.get_tilemap_collision(tilemap):
            self.x = prev_x
            self.velocity[0]*=-self.restitution_coefficient

        prev_y = self.y
        self.y+=self.velocity[1]*self.ui.deltatime
        if self.get_tilemap_collision(tilemap):
            self.y = prev_y
            self.velocity[1]*=-self.restitution_coefficient
        

        if self.get_pressed('SHOOT'):
            self.shoot(projectiles)
    
    def get_pressed(self,code):
        if code in self.keybinds:
            for k in self.keybinds[code]:
                if self.ui.kprs[k]:
                    return True
        return False


        
