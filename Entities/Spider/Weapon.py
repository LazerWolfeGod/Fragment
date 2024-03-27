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
        self.reload_time = stats['Reload']
        self.max_rounds = stats['Rounds']
        self.optimal_range = stats['Optimal_Range']
        
        self.projectile_dict = {'Energy_Ball':Energy_Ball,
                                'Bullet':Bullet,
                                'Fire':Fire,
                                'Laser':Laser,
                                'Pellet':Pellet,
                                'Wave':Wave,
                                'Melee':Melee}

        self.projectile_obj = self.projectile_dict[self.projectile_type]

        self.cooldown_timer = 0
        self.reload_timer = 0
        self.reloading = False
        self.stored_rounds = self.max_rounds
        
        self.angle = 0
        self.angular_velocity = 0
        self.turn_acceleration = 0.3
        
        self.image = Data.Weapons[self.weapon_name]['Image']
        self.image = pygame.transform.scale_by(self.image,(self.length)/(self.image.get_width()-self.image.get_height()))


    def shoot(self,projectiles,ui,x,y,vel,team):
        if not self.reloading:
            if self.cooldown_timer<0:
                self.cooldown_timer = self.cooldown
                dis = 1*self.length
                player_speed_component = ((vel[0]*math.cos(self.angle))**2+(vel[1]*math.sin(self.angle))**2)**0.5
                if self.projectile_type == 'Wave':
                    spread = 1
                    for a in range(7):
                        projectiles.append(self.projectile_obj(ui,x+math.cos(self.angle)*dis,
                                     y+math.sin(self.angle)*dis,self.angle+((a-3)/7)*spread,
                                     self.shot_velocity-player_speed_component,team,self.damage))
                else:
                    projectiles.append(self.projectile_obj(ui,x+math.cos(self.angle)*dis,
                                     y+math.sin(self.angle)*dis,random.gauss(self.angle,self.accuracy),
                                     self.shot_velocity-player_speed_component,team,self.damage))
                self.stored_rounds-=1
                if self.stored_rounds == 0:
                    self.reload()
                return self.kick_back
        return 0
    
    def reload(self):
        self.reload_timer = self.reload_time
        self.reloading = True
        self.stored_rounds = self.max_rounds
    def render(self,Surf,center):
        rotated = pygame.transform.rotate(self.image,-self.angle/math.pi*180)
        offset = [self.length*math.cos(self.angle)*0.55,self.length*math.sin(self.angle)*0.55]
        Surf.blit(rotated,[center[0]-rotated.get_width()/2+offset[0],center[1]-rotated.get_height()/2+offset[1]])
    def render_hud(self,Surf):
        if self.max_rounds>100:
            wid = int(400/self.max_rounds)
            gap = 0
        else:
            wid = min(50,400/self.max_rounds)
            gap = min(2,wid/8)
        pyui.draw.rect(Surf,(50,10,10),pygame.Rect(10,10,wid*self.max_rounds,50),border_radius=10)
        for a in range(self.stored_rounds):
            pyui.draw.rect(Surf,(103,95,92),pygame.Rect(10+gap+wid*a,10+gap,wid-gap*2,50-gap*2),border_radius=10)
        if self.reloading:
            pygame.draw.rect(Surf,(50,10,10),pygame.Rect(10+(wid*self.max_rounds)*(1-self.reload_timer/self.reload_time),
                                                       10,wid*self.max_rounds*(self.reload_timer/self.reload_time),48),border_radius=10)

    def gametick(self,deltatime,target_angle):
        self.angle = target_angle
        self.cooldown_timer-=deltatime
        self.reload_timer-=deltatime
        if self.reload_timer<0:
            self.reloading = False
