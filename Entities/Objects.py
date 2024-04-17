import pygame,json
pygame.init()

from Data.Object_Data import Object_Data
from Utility_functions import *
from Entities.Entity import Entity



class Object(Entity):
    def __init__(self,ui,x,y,angle,name):
        super().__init__(ui,x,y)
        self.thing = 'Object'
        self.team = 'None'
        
        self.name = name
        self.stats = Object_Data.objects[self.name]['Stats']
        self.width = self.stats['Width']
        self.height = self.stats['Height']
        self.mass = self.stats['Mass']
        self.health = self.stats['Health']
        self.max_health = self.health


        self.base_image = Object_Data.objects[self.name]['Image'].copy()
        self.image = pygame.transform.scale(self.base_image,(self.width,self.height))
        self.image = pygame.transform.rotate(self.image,self.angle)
        

    def render_surf(self):
        return self.image

    def get_hitboxes(self):
        return [(self.x-self.width/2,self.y-self.height/2,self.width,self.height)]


class Box(Object):
    def __init__(self,ui,x,y,angle=0):
        super().__init__(ui,x,y,angle,'Box')
        
