import pygame
pygame.init()

from Utility_functions import *


class Object_Data:
    objects = {'Box':{'File':'Assets\\Box.png',
                      'Stats':{'Width':60,'Height':60,'Health':50,'Mass':0.1}}}

    for obj in objects:
        objects[obj]['Image'] = pygame.image.load(resourcepath(objects[obj]['File'])).convert_alpha()
    
