import pygame,math,random
import PyUI as pyui
from Physics_Objects.Projectile import *
from Utility_functions import *
from Entities.Spider.Spider_Data import Data

class Weapon:
    def __init__(self,weapon_name):
        self.weapon_name = weapon_name
        
        stats = Data.Weapons[self.weapon_name]['Stats']
        self.length = stats['Length']
        self.projectile_type = stats['Projectile']
        self.kick_back = stats['Kick_Back']
        self.cooldown = stats['Cooldown']
        self.autofire = stats['AutoFire']
        self.damage = stats['Damage']
        self.accuracy = stats['Accuracy']
        self.shot_velocity = stats['Velocity']
        
        
        self.projectile_dict = {'Energy_Ball':Energy_Ball,
                                'Bullet':Bullet,
                                'Fire':Fire,
                                'Laser':Laser}

        self.projectile_obj = self.projectile_dict[self.projectile_type]

        self.cooldown_tracker = 0
        self.angle = 0
        self.angular_velocity = 0
        self.turn_acceleration = 0.3
        
        self.image = Data.Weapons[self.weapon_name]['Image']
        self.image = pygame.transform.scale_by(self.image,(self.length)/(self.image.get_width()-self.image.get_height()))


    def shoot(self,projectiles,ui,x,y,vel,team):
        if self.cooldown_tracker<0:
            self.cooldown_tracker = self.cooldown
            dis = 1*self.length
            player_speed_component = ((vel[0]*math.cos(self.angle))**2+(vel[1]*math.sin(self.angle))**2)**0.5
            projectiles.append(self.projectile_obj(ui,x+math.cos(self.angle)*dis,
                                 y+math.sin(self.angle)*dis,random.gauss(self.angle,self.accuracy),
                                 self.shot_velocity-player_speed_component,team))
            return self.kick_back
        return 0
    

    def render(self,Surf,center):
        rotated = pygame.transform.rotate(self.image,-self.angle/math.pi*180)
        offset = [self.length*math.cos(self.angle)*0.55,self.length*math.sin(self.angle)*0.55]
        Surf.blit(rotated,[center[0]-rotated.get_width()/2+offset[0],center[1]-rotated.get_height()/2+offset[1]])

    def gametick(self,deltatime,target_angle):
        self.angle = target_angle
        self.cooldown_tracker-=deltatime
