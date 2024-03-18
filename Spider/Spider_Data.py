import pygame
pygame.init()

from Utility_functions import *

class Data:
    # overlay string: n = not this tile, a = any tile, t = this tile

    Sounds = {'Footstep':pygame.mixer.Sound('Assets\\Audio\\Footstep.wav')}
    

    Legs = {'Base':{'File':'Assets\\Player_parts\\legs\\Leg.png',
                    'Stats':{'Length':21,'Target_Distance':30,'Num_Legs':4,
                             'Move_Speed':0.3,'Move_Friction':0.85,'Turn_Speed':0.2}},
            'Blue':{'File':'Assets\\Player_parts\\Legs\\Blue.png',
                     'Stats':{'Length':20,'Target_Distance':30,'Num_Legs':4,
                              'Move_Speed':0.45,'Move_Friction':0.85,'Turn_Speed':0.2}},
            'Red':{'File':'Assets\\Player_parts\\Legs\\Red.png',
                   'Stats':{'Length':30,'Target_Distance':45,'Num_Legs':6,
                            'Move_Speed':0.8,'Move_Friction':0.85,'Turn_Speed':0.3}}}

    Bodies = {'Base':{'File':'Assets\\Player_parts\\Bodies\\Base.png',
                      'Stats':{'Radius':15}},
              'Blue':{'File':'Assets\\Player_parts\\Bodies\\Blue.png',
                      'Stats':{'Radius':20}},
              'Red':{'File':'Assets\\Player_parts\\Bodies\\Red.png',
                      'Stats':{'Radius':25}}}

    Weapons = {'Blaster':{'File':'Assets\\Player_parts\\Weapons\\Blaster.png',
                          'Stats':{'Length':30,'Projectile':'Energy_Ball','Kick_Back':0.05,'Cooldown':20,'AutoFire':False,
                                   'Damage':3,'Accuracy':0.05,'Velocity':12}},
               'Base':{'File':'Assets\\Player_parts\\Weapons\\Base.png',
                          'Stats':{'Length':30,'Projectile':'Bullet','Kick_Back':1,'Cooldown':10,'AutoFire':False,
                                   'Damage':1,'Accuracy':0.1,'Velocity':10}},
               'Flamer':{'File':'Assets\\Player_parts\\Weapons\\Flamer.png',
                         'Stats':{'Length':50,'Projectile':'Fire','Kick_Back':0.1,'Cooldown':0,'AutoFire':True,
                                  'Damage':1,'Accuracy':0.3,'Velocity':10}}}
    
    def load_images():
        for leg in Data.Legs:
            Data.Legs[leg]['Image'] = pygame.image.load(Data.Legs[leg]['File']).convert_alpha()
        for Body in Data.Bodies:
            Data.Bodies[Body]['Image'] = pygame.image.load(Data.Bodies[Body]['File']).convert_alpha()
        for Weapon in Data.Weapons:
            Data.Weapons[Weapon]['Image'] = pygame.image.load(Data.Weapons[Weapon]['File']).convert_alpha()



Data.load_images()


