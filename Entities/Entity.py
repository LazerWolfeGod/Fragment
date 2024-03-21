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

        self.move_friction = 0.85
        self.restitution_coefficient = 0.5

        
    def get_map_collision(self,mapp=0):
        if mapp != 0:
            for h in self.get_hitboxes():
                if mapp.check_collisions(h):
                    return True
        return False
    def get_hitboxes(self):
        return [(self.x,self.y,self.radius)]

    def get_collide(self,obj):
        return list_obj_collide(self.get_hitboxes(),obj)

    def take_damage(self,damage,impact_vel=-1,knockback=0):
        if self.immunity_frames<0:
            if impact_vel != -1:
                self.velocity+=(impact_vel*knockback)/self.mass
            self.immunity_frames = 1
            self.health-=damage
            self.angular_velocity+=random.gauss(0,20*knockback/self.mass)
            
    def check_dead(self,particles):
        self.dead = True
        if self.health<0:
            return True
        return False

    def gametick(self,mapp,projectiles,entities,deltatime):
        self.move(mapp,deltatime)
    
    def move(self,mapp,deltatime):
        self.child_move(mapp,deltatime)
        self.immunity_frames-=deltatime

        self.velocity*=self.move_friction**self.ui.deltatime

        self.angular_velocity*=0.3
        self.angle+=self.angular_velocity

        prev_x = self.x
        self.x+=self.velocity[0]*self.ui.deltatime
        if self.get_map_collision(mapp):
            self.x = prev_x
            self.velocity[0]*=-self.restitution_coefficient

        prev_y = self.y
        self.y+=self.velocity[1]*self.ui.deltatime
        if self.get_map_collision(mapp):
            self.y = prev_y
            self.velocity[1]*=-self.restitution_coefficient

##        if self.thing == 'Spider':
##            self.spider_physics(self.ui.deltatime)

            

    def child_move(self,_,__): pass

        
