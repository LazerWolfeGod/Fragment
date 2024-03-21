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

        self.image = Data.Weapons[self.weapon_name]['Image']
        self.image = pygame.transform.scale_by(self.image,(self.length)/(self.image.get_width()-self.image.get_height()))


    def shoot(self,projectiles,ui,x,y,angle,vel,team):
        if self.cooldown_tracker<0:
            self.cooldown_tracker = self.cooldown
            dis = 1*self.length
            player_speed_component = ((vel[0]*math.cos(angle))**2+(vel[1]*math.sin(angle))**2)**0.5
            projectiles.append(self.projectile_obj(ui,x+math.cos(angle)*dis,
                                 y+math.sin(angle)*dis,random.gauss(angle,self.accuracy),
                                 self.shot_velocity-player_speed_component,team))
            return self.kick_back
        return 0
    

    def render(self,Surf,center,player_angle):
        rotated = pygame.transform.rotate(self.image,-player_angle/math.pi*180)
        offset = [self.length*math.cos(player_angle)*0.55,self.length*math.sin(player_angle)*0.55]
        Surf.blit(rotated,[center[0]-rotated.get_width()/2+offset[0],center[1]-rotated.get_height()/2+offset[1]])

    def gametick(self,deltatime):
        self.cooldown_tracker-=deltatime
        
##    def make_energy_ball(self,projectiles,ui,x,y,angle,speed):
##        projectiles.append(Energy_Ball(ui,x,y,angle),speed)
##    def make_bullet(self,projectiles,ui,x,y,angle):
##        projectiles.append(Bullet(ui,x,y,angle))
##    def make_fire(self,projectiles,ui,x,y,angle):
##        projectiles.append(Fire(ui,x,y,angle))
##    def make_laser(self,projectiles,ui,x,y,angle):
##        projectiles.append(Laser(ui,x,y,angle))
