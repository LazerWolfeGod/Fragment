import pygame,math,random
import PyUI as pyui
from Projectile import *


class Player:
    def __init__(self,ui,x,y):
        self.ui = ui
        self.x = x
        self.y = y
        self.velocity = [0,0]
        self.angle = 0
        self.target_angle = 0
        
        self.move_acceleration = 1
        self.move_friction = 0.85
        self.turn_acceleration = 1
        self.restitution_coefficient = 0.2
        
        
        self.keybinds = {'UP':[pygame.K_w,pygame.K_UP],
                         'DOWN':[pygame.K_s,pygame.K_DOWN],
                         'LEFT':[pygame.K_a,pygame.K_LEFT],
                         'RIGHT':[pygame.K_d,pygame.K_RIGHT],
                         'SHOOT':[pygame.K_SPACE],
                         'DASH':[pygame.K_SPACE]}

        self.mpos = (0,0)
        
    def render_surf(self):
        radius = 15
        self.radius = radius
        Surf = pygame.Surface((radius*4,radius*4),pygame.SRCALPHA)
        pygame.draw.circle(Surf,(150,100,60),(radius*2,radius*2),radius)
        pygame.draw.line(Surf,(180,120,60),(radius*2,radius*2),(radius*2+math.cos(self.angle)*self.radius*1.5,
                                                                radius*2+math.sin(self.angle)*self.radius*1.5),int(self.radius/3))
        return Surf

    def control(self,tilemap,projectiles):
        if self.get_pressed('UP'): self.velocity[1]-=self.move_acceleration*self.ui.deltatime
        if self.get_pressed('DOWN'): self.velocity[1]+=self.move_acceleration*self.ui.deltatime
        if self.get_pressed('LEFT'): self.velocity[0]-=self.move_acceleration*self.ui.deltatime
        if self.get_pressed('RIGHT'): self.velocity[0]+=self.move_acceleration*self.ui.deltatime

        self.angle = math.atan2(self.mpos[1]-self.y,self.mpos[0]-self.x)

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

    def shoot(self,projectiles):
        projectiles.append(Fader(self.ui,self.x,self.y,self.angle+random.gauss(0,0.1)))

    def get_tilemap_collision(self,tilemap):
        return tilemap.check_collisions((self.x,self.y,self.radius))

    
        
