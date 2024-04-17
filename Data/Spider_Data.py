import pygame
pygame.init()

from Utility_functions import *

class Spider_Data:
    # overlay string: n = not this tile, a = any tile, t = this tile

    Sounds = {'Footstep':pygame.mixer.Sound('Assets\\Audio\\Footstep.wav')}

    Leg_default_stats = {'Length':30,'Target_Distance':45,'Num_Legs':4,
                         'Move_Speed':0.3,'Move_Friction':0.85,'Turn_Speed':0.2,
                         'Joint_Rotate_Speed':0.3,'Forward_Value':1,
                         'Lift_Up_Distance_Max':0.6,'Lift_Up_Distance_Min':0.3,
                         'Prediction_Magnitude_Velocity':8,'Prediction_Magnitude_Angle':8}

    Legs = {'Base':{'File':'Assets\\Player_parts\\legs\\Leg.png',
                    'Stats':{'Length':21,'Target_Distance':30,'Num_Legs':4,'Move_Speed':0.3,'Turn_Speed':0.2}},
            
            'Blue':{'File':'Assets\\Player_parts\\Legs\\Blue.png',
                     'Stats':{'Length':22,'Target_Distance':34,'Num_Legs':4,'Move_Speed':0.45,
                              'Turn_Speed':0.15,'Prediction_Magnitude_Velocity':7}},
            
            'Red':{'File':'Assets\\Player_parts\\Legs\\Red.png',
                   'Stats':{'Length':30,'Target_Distance':45,'Num_Legs':6,
                            'Move_Speed':0.8,'Turn_Speed':0.2,
                            'Forward_Value':0.95,'Prediction_Magnitude_Velocity':6}},
            
            'Green':{'File':'Assets\\Player_parts\\Legs\\Green.png',
                   'Stats':{'Length':80,'Target_Distance':140,'Num_Legs':8,
                            'Move_Speed':0.8,'Move_Friction':0.85,'Turn_Speed':0.05,
                            'Joint_Rotate_Speed':0.1,'Foward_Value':0.97}},
            'Metal':{'File':'Assets\\Player_parts\\Legs\\Metal.png',
                   'Stats':{'Length':30,'Target_Distance':50,'Num_Legs':4,
                            'Move_Speed':0.5,'Turn_Speed':0.2}},
            }

    Bodies = {'Base':{'File':'Assets\\Player_parts\\Bodies\\Base.png',
                      'Stats':{'Radius':15,'Mass':5,'Health':20}},
              'Blue':{'File':'Assets\\Player_parts\\Bodies\\Blue.png',
                      'Stats':{'Radius':20,'Mass':10,'Health':30}},
              'Red':{'File':'Assets\\Player_parts\\Bodies\\Red.png',
                      'Stats':{'Radius':25,'Mass':20,'Health':50}},
              'Four':{'File':'Assets\\Player_parts\\Bodies\\4.png',
                      'Stats':{'Radius':30,'Mass':30,'Health':70}},
              'Green':{'File':'Assets\\Player_parts\\Bodies\\Green.png',
                      'Stats':{'Radius':64,'Mass':200,'Health':500}},
              'Metal':{'File':'Assets\\Player_parts\\Bodies\\Metal.png',
                      'Stats':{'Radius':25,'Mass':20,'Health':50}},
              }

    Weapons = {'Base':{'File':'Assets\\Player_parts\\Weapons\\Base.png',
                          'Stats':{'Length':20,'Projectile':'Pellet','Kick_Back':5,'Cooldown':30,'AutoFire':False,
                                   'Damage':1,'Accuracy':0.15,'Velocity':6,'Rounds':4,'Reload':90,'Optimal_Range':200}},
               'Pellet_Shooter':{'File':'Assets\\Player_parts\\Weapons\\Pellet_Shooter.png',
                          'Stats':{'Length':20,'Projectile':'Pellet','Kick_Back':0.05,'Cooldown':15,'AutoFire':False,
                                   'Damage':1,'Accuracy':0.25,'Velocity':7,'Rounds':5,'Reload':60,'Optimal_Range':100}},
               'Blade':{'File':'Assets\\Player_parts\\Weapons\\Blade.png',
                          'Stats':{'Length':35,'Projectile':'Melee','Kick_Back':0,'Cooldown':0,'AutoFire':True,
                                   'Damage':0.2,'Accuracy':0,'Velocity':0,'Rounds':10,'Reload':0,'Optimal_Range':50}},
               'Blaster':{'File':'Assets\\Player_parts\\Weapons\\Blaster.png',
                          'Stats':{'Length':30,'Projectile':'Energy_Ball','Kick_Back':0.05,'Cooldown':20,'AutoFire':False,
                                   'Damage':3,'Accuracy':0.05,'Velocity':12,'Rounds':5,'Reload':60,'Optimal_Range':200}},
               'Rapid':{'File':'Assets\\Player_parts\\Weapons\\Rapid.png',
                          'Stats':{'Length':30,'Projectile':'Bullet','Kick_Back':5,'Cooldown':10,'AutoFire':False,
                                   'Damage':1,'Accuracy':0.1,'Velocity':10,'Rounds':15,'Reload':120,'Optimal_Range':200}},
               'Rifle':{'File':'Assets\\Player_parts\\Weapons\\Rifle.png',
                          'Stats':{'Length':25,'Projectile':'Bullet','Kick_Back':15,'Cooldown':30,'AutoFire':False,
                                   'Damage':5,'Accuracy':0.01,'Velocity':15,'Rounds':10,'Reload':90,'Optimal_Range':400}},
               'Waver':{'File':'Assets\\Player_parts\\Weapons\\Waver.png',
                          'Stats':{'Length':25,'Projectile':'Wave','Kick_Back':15,'Cooldown':30,'AutoFire':False,
                                   'Damage':3,'Accuracy':0,'Velocity':15,'Rounds':5,'Reload':60,'Optimal_Range':200}},
               'Flamer':{'File':'Assets\\Player_parts\\Weapons\\Flamer.png',
                         'Stats':{'Length':50,'Projectile':'Fire','Kick_Back':1,'Cooldown':0,'AutoFire':True,
                                  'Damage':1,'Accuracy':0.3,'Velocity':10,'Rounds':150,'Reload':100,'Optimal_Range':200}},
               'Mini_Gun':{'File':'Assets\\Player_parts\\Weapons\\Mini_Gun.png',
                           'Stats':{'Length':45,'Projectile':'Bullet','Kick_Back':5,'Cooldown':0,'AutoFire':True,
                                  'Damage':3,'Accuracy':0.2,'Velocity':15,'Rounds':200,'Reload':200,'Optimal_Range':200}},
               'Laser':{'File':'Assets\\Player_parts\\Weapons\\Laser.png',
                           'Stats':{'Length':45,'Projectile':'Laser','Kick_Back':50,'Cooldown':0,'AutoFire':True,
                                  'Damage':2,'Accuracy':0,'Velocity':33,'Rounds':300,'Reload':60,'Optimal_Range':400}},
               }


    for leg in Legs:
        for s in Leg_default_stats:
            if not s in Legs[leg]['Stats']:
                Legs[leg]['Stats'][s] = Leg_default_stats[s]
        
    
    def load_images():
        for leg in Spider_Data.Legs:
            Spider_Data.Legs[leg]['Image'] = pygame.image.load(Spider_Data.Legs[leg]['File']).convert_alpha()
        for Body in Spider_Data.Bodies:
            Spider_Data.Bodies[Body]['Image'] = pygame.image.load(Spider_Data.Bodies[Body]['File']).convert_alpha()
        for Weapon in Spider_Data.Weapons:
            Spider_Data.Weapons[Weapon]['Image'] = pygame.image.load(Spider_Data.Weapons[Weapon]['File']).convert_alpha()



Spider_Data.load_images()


