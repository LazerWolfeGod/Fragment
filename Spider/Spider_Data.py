import pygame
pygame.init()

from Utility_functions import *

class Data:
    # overlay string: n = not this tile, a = any tile, t = this tile
    

    Legs = {'Base':{'File':'Assets\\Player_parts\\legs\\Leg.png',
                    'Stats':{'Length':21,'Target_Distance':30,'Num_Legs':4}},
            'Leg 2':{'File':'Assets\\Player_parts\\Legs\\Leg 2.png',
                     'Stats':{'Length':25,'Target_Distance':35,'Num_Legs':4}}}

    Bodies = {'Base':{'File':'Assets\\Player_parts\\Bodies\\Base.png',
                      'Stats':{'Radius':15}}}

    Weapons = {'Blaster':{'File':'Assets\\Player_parts\\Weapons\\Blaster.png',
                          'Stats':{'Length':30,'Projectile':'Energy_Ball'}}}
    
    def load_images():
        for leg in Data.Legs:
            Data.Legs[leg]['Image'] = pygame.image.load(Data.Legs[leg]['File']).convert_alpha()
        for Body in Data.Bodies:
            Data.Bodies[Body]['Image'] = pygame.image.load(Data.Bodies[Body]['File']).convert_alpha()
        for Weapon in Data.Weapons:
            Data.Weapons[Weapon]['Image'] = pygame.image.load(Data.Weapons[Weapon]['File']).convert_alpha()



Data.load_images()


