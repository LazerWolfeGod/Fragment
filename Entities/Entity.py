import pygame,math,random
import PyUI as pyui

from Utility_functions import *

class Entity:
    def __init__(self,ui,x,y):
        self.thing = 'Entity'
        self.ui = ui
        self.x = x
        self.y = y
        self.velocity = pygame.Vector2()
        self.angular_velocity = 0
        self.angle = 0
        self.immunity_frames = 0
        
        self.dead = False
        self.active = True
        self.colgrid_IDs = set()

        self.move_friction = 0.85
        self.restitution_coefficient = 0.5

        self.time_since_damage = 0
        self.heal_rate = -1
        self.time_to_heal = 200
        
    def check_collision(self,mapp=0,entity_collide_dict={}):
        if mapp != 0:
            for h in self.get_hitboxes():
                if mapp.check_collisions(h):
                    return True
        for i in self.colgrid_IDs:
            for e in entity_collide_dict[i]:
                if e!=self and e.get_collide(self.get_hitboxes()[0]):
                    
                    return True
        return False
    def get_hitboxes(self):
        return [(self.x,self.y,self.radius)]

    def get_collide(self,obj):
        return list_obj_collide(self.get_hitboxes(),obj)

    def get_vel_mag(self):
        return ((self.velocity[0])**2+(self.velocity[1])**2)**0.5
    def get_vel_angle(self):
        return math.atan2(self.velocity[1],self.velocity[0])

    def take_damage(self,damage,impact_vel=-1,knockback=0):
        if self.immunity_frames<0:
            if impact_vel != -1:
                self.velocity+=(impact_vel*knockback)/self.mass
            self.immunity_frames = 1
            self.health-=damage
            self.angular_velocity+=random.gauss(0,20*knockback/self.mass)
            self.time_since_damage = 0
            
    def check_dead(self,particles):
        self.dead = True
        if self.health<0:
            self.die(particles)
            return True
        return False
    def die(self,_): pass

    def gametick(self,mapp,projectiles,entity_collide_dict,entities,deltatime):
        self.heal(deltatime)
        self.move(mapp,entity_collide_dict,deltatime)
    def heal(self,deltatime):
        self.time_since_damage+=deltatime
        if self.heal_rate!=-1 and self.time_since_damage>self.time_to_heal:
            self.health = min(self.health+(2**(min(self.time_since_damage-self.time_to_heal,600)*self.heal_rate/60))/60*deltatime,self.max_health)

    def move(self,mapp,entity_collide_dict,deltatime):
        self.child_move(mapp,deltatime)
        self.immunity_frames-=deltatime

        self.velocity*=self.move_friction**self.ui.deltatime

        self.angular_velocity*=0.3
        self.angle+=self.angular_velocity

        prev_x = self.x
        self.x+=self.velocity[0]*self.ui.deltatime
        if self.check_collision(mapp,entity_collide_dict):
            self.x = prev_x
            self.velocity[0]*=-self.restitution_coefficient

        prev_y = self.y
        self.y+=self.velocity[1]*self.ui.deltatime
        if self.check_collision(mapp,entity_collide_dict):
            self.y = prev_y
            self.velocity[1]*=-self.restitution_coefficient

            

    def child_move(self,_,__): pass

        
