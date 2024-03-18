import pygame
pygame.init()

from Utility_functions import *

class Data:

    physics_defaults = {'Restitution':1,'Drag':1,'Collision_Limit':0}
    
    
    projectiles = {'Bullet':{'File':'Assets\\Projectiles\\Bullet.png',
                             'Stats':{'Width':11,'Restitution':1}},
                   'Energy_Ball':{'File':'Assets\\Projectiles\\Energy_Ball.png',
                                  'Stats':{'Width':12}},
                   'Fire':{'File':'Assets\\Projectiles\\Fire.png',
                           'Stats':{'Width':12,'Restitution':0.2,'Drag':0.98,'Collision_Limit':1}}}

    particles = {'Spark':{'File':'Assets\\Particles\\Spark.png',
                          'Stats':{'Width':10,'Restitution':1,'Drag':0.9}}}
    
    def load_images():
        for p in Data.projectiles:
            Data.projectiles[p]['Image'] = pygame.image.load(Data.projectiles[p]['File']).convert_alpha()
        for p in Data.particles:
            Data.particles[p]['Image'] = pygame.image.load(Data.particles[p]['File']).convert_alpha()
        
Data.load_images()

