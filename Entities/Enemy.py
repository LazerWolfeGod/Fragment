import pygame,math,random
import PyUI as pyui

from Utility_functions import *
from Entities.Spider.Spider import Spider 

class Enemy(Spider):
    def __init__(self,ui,x,y,leg_name='Base',body_name='Base',weapon_name='Base'):
        self.team = 'Enemy'
        super().__init__(ui,x,y,leg_name,body_name,weapon_name)

        self.attack_target = -1

        self.passive_move_timer = 0
        self.move_length = 0
        
        self.move_vector = pygame.Vector2(0,0)


    def control(self,mapp,projectiles,entities):

        if self.attack_target == -1:
            min_dis = 500
            for e in entities:
                if e.team != self.team:
                    dis = ((self.x-e.x)**2+(self.y-e.y)**2)**0.5
                    if dis<min_dis:
                        self.attack_target = e
                        min_dis = dis
        

        if self.attack_target != -1:
            self.move_vector = pygame.Vector2(0,0)
            self.target_body_angle = math.atan2(self.attack_target.y-self.y,self.attack_target.x-self.x)
            
            self.shoot(projectiles)
        else:
            self.passive_move_timer+=self.ui.deltatime
            self.move_length-=self.ui.deltatime
            if self.move_length<0:
                self.move_vector = pygame.Vector2(0,0)
            if random.random()<0.02 and self.passive_move_timer>random.gauss(300,100):
                self.move_vector = pygame.Vector2(random.random()-0.5,random.random()-0.5)
                self.passive_move_timer = 0
                self.target_body_angle = math.atan2(self.move_vector[1],self.move_vector[0])
                self.move_length = random.gauss(60,20)
                


        
    


        
