import pygame,math,random
from Utility_functions import *
from Entities.Spider.Spider_Data import Data

class Body:
    def __init__(self,body_name):
        self.body_name = body_name
        stats = Data.Bodies[self.body_name]['Stats']

        self.radius = stats['Radius']
        self.mass = stats['Mass']
        self.health = stats['Health']
        self.base_image = Data.Bodies[self.body_name]['Image']
        self.image = pygame.transform.scale(self.base_image,(self.radius*2,self.radius*2))

    
    def render(self,Surf,center,player_angle):
        rotated = pygame.transform.rotate(self.image,-player_angle/math.pi*180)
        Surf.blit(rotated,[center[0]-rotated.get_width()/2,center[1]-rotated.get_height()/2])
