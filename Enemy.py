import pygame,math,random
import PyUI as pyui

from Utility_functions import *
from Spider.Spider import Spider 

class Enemy(Spider):
    def __init__(self,ui,x,y):
        self.team = 'Enemy'
        super().__init__(ui,x,y,'Blue','Blue','Base')

        self.attack_target = -1


    def control(self,tilemap,projectiles,entities):

        if self.attack_target == -1:
            min_dis = math.inf
            for e in entities:
                if e.team != self.team:
                    dis = ((self.x-e.x)**2+(self.y-e.y)**2)**0.5
                    if dis<min_dis:
                        self.attack_target = e
                        min_dis = dis
        
        self.move_vector = pygame.Vector2(0,0)

        if self.attack_target != -1:
            self.target_angle = math.atan2(self.attack_target.y-self.y,self.attack_target.x-self.x)
            
            self.shoot(projectiles)


        
    


        
