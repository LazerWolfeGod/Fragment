import pygame
pygame.init()

from Utility_functions import *

class Data:

    physics_defaults = {'Restitution':1,'Drag':1,'Collision_Limit':0,'Has_Collisions':True}
    
    
    projectiles = {'Bullet':{'File':'Assets\\Projectiles\\Bullet.png',
                           'Stats':{'Damage':1,'Knockback':0.1,'Width':11,'Restitution':1}},
                   'Energy_Ball':{'File':'Assets\\Projectiles\\Energy_Ball.png',
                           'Stats':{'Damage':1,'Knockback':0.1,'Width':12}},
                   'Fire':{'File':'Assets\\Projectiles\\Fire.png',
                           'Stats':{'Damage':1,'Knockback':0.1,'Width':12,'Restitution':0.2,'Drag':0.98,'Collision_Limit':1}},
                   'Laser':{'File':'Assets\\Projectiles\\Laser.png',
                           'Stats':{'Damage':1,'Knockback':0.2,'Width':8,'Restitution':1,'Drag':0.999,'Collision_Limit':3}},
                   }

    particles = {'Spark':{'File':'Assets\\Particles\\Spark.png',
                          'Stats':{'Width':10,'Restitution':1,'Drag':0.9}},
                 'Laser_Dust':{'File':'Assets\\Particles\\Laser_Dust.png',
                          'Stats':{'Width':10,'Drag':0.9,'Has_Collisions':False}},
                 'Dust':{'File':'Assets\\Particles\\Dust.png',
                          'Stats':{'Width':(6,2),'Drag':0.8,'Has_Collisions':False}},
                 
                 }
    
    def load_images():
        for p in Data.projectiles:
            Data.projectiles[p]['Image'] = pygame.image.load(Data.projectiles[p]['File']).convert_alpha()
        for p in Data.particles:
            Data.particles[p]['Image'] = pygame.image.load(Data.particles[p]['File']).convert_alpha()
        
Data.load_images()

