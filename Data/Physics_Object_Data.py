import pygame
pygame.init()

from Utility_functions import *

class Physics_Object_Data:

    physics_defaults = {'Restitution':1,'Drag':1,'Collision_Limit':0,'Has_Collisions':True}
    
    
    projectiles = {'Pellet':{'File':'Assets\\Projectiles\\Pellet.png',
                             'Stats':{'Knockback':0.1,'Width':10,'Drag':0.9}},
                   'Bullet':{'File':'Assets\\Projectiles\\Bullet.png',
                           'Stats':{'Knockback':0.1,'Width':11,'Restitution':1,'Collision_Limit':0}},
                   'Energy_Ball':{'File':'Assets\\Projectiles\\Energy_Ball.png',
                           'Stats':{'Knockback':0.1,'Width':12}},
                   'Wave':{'File':'Assets\\Projectiles\\Wave.png',
                             'Stats':{'Knockback':0.1,'Width':33,'Drag':0.75}},
                   'Fire':{'File':'Assets\\Projectiles\\Fire.png',
                           'Stats':{'Knockback':0.1,'Width':12,'Restitution':0.2,'Drag':0.98,'Collision_Limit':1}},
                   'Laser':{'File':'Assets\\Projectiles\\Laser.png',
                           'Stats':{'Knockback':0.2,'Width':8,'Restitution':1,'Drag':0.999,'Collision_Limit':3}},
                   'Melee':{'File':'Assets\\Projectiles\\Melee.png',
                           'Stats':{'Knockback':0.2,'Width':20,'Restitution':1,'Drag':0,'Collision_Limit':0}},
                   }

    particles = {'Spark':{'File':'Assets\\Particles\\Spark.png',
                          'Stats':{'Width':10,'Restitution':1,'Drag':0.9}},
                 'Laser_Dust':{'File':'Assets\\Particles\\Laser_Dust.png',
                          'Stats':{'Width':10,'Drag':0.9,'Has_Collisions':False}},
                 'Dust':{'File':'Assets\\Particles\\Dust.png',
                          'Stats':{'Width':(6,2),'Drag':0.8,'Has_Collisions':False}},
                 'Spider_Body':{'File':'Assets\\Player_Parts\\Bodies\\Base.png',
                          'Stats':{'Width':40,'Drag':0.9,'Has_Collisions':True,'Collision_Limit':4}},
                 'Spider_Leg':{'File':'Assets\\Player_Parts\\Bodies\\Base.png',
                          'Stats':{'Width':40,'Drag':0.9,'Has_Collisions':True,'Collision_Limit':4}},
                 
                 }
    
    def load_images():
        for p in Physics_Object_Data.projectiles:
            Physics_Object_Data.projectiles[p]['Image'] = pygame.image.load(Physics_Object_Data.projectiles[p]['File']).convert_alpha()
        for p in Physics_Object_Data.particles:
            Physics_Object_Data.particles[p]['Image'] = pygame.image.load(Physics_Object_Data.particles[p]['File']).convert_alpha()
        
Physics_Object_Data.load_images()

