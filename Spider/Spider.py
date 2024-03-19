import pygame,math,random
from Utility_functions import *
from Spider.Spider_Data import Data
from Spider.Leg import Leg
from Spider.Body import Body
from Spider.Weapon import Weapon

class Spider:
    def __init__(self,leg_name,body_name,weapon_name):
        self.leg_name = leg_name
        self.body_name = body_name
        self.weapon_name = weapon_name

        self.make_body()
        self.radius = self.body.radius
        
        self.make_legs()
        self.make_weapon()

        self.move_acceleration = self.legs[0].move_speed # 0.5
        self.move_friction = self.legs[0].move_friction # 0.85
        self.turn_acceleration = self.legs[0].turn_speed # 0.2
        self.restitution_coefficient = 0.2

        
    def make_legs(self):
        self.num_legs = Data.Legs[self.leg_name]['Stats']['Num_Legs']
        self.legs = [Leg([self.x,self.y],self.angle,theta/self.num_legs*math.tau+math.pi/self.num_legs,
                         self.leg_name,self.radius,1) for theta in range(self.num_legs)]
    def make_body(self):
        self.body = Body(self.body_name)
    def make_weapon(self):
        self.weapon = Weapon(self.weapon_name)
    
    def render_surf(self):
        center = (self.radius*20,self.radius*20)
        Surf = pygame.Surface((self.radius*40,self.radius*40),pygame.SRCALPHA)

        self.body.render(Surf,center,self.angle)  
        for leg in self.legs:
            leg.render(Surf,center,self.angle)

        self.weapon.render(Surf,center,self.angle)
        return Surf

    def get_tilemap_collision(self,tilemap=0):
        if tilemap != 0:
            return tilemap.check_collisions((self.x,self.y,self.radius))
        return False

    
    def shoot(self,projectiles):
        kickback = self.weapon.shoot(projectiles,self.ui,self.x,self.y,self.angle)

        self.velocity[0]-=kickback*math.cos(self.angle)
        self.velocity[1]-=kickback*math.sin(self.angle)
    
    def move_spider(self,tilemap,deltatime):
        for i,leg in enumerate(self.legs):
            on_ground = [l.on_ground for l in self.legs]
            can_lift = sum(on_ground)>int(len(self.legs)/2) and (self.legs[(i-1)%len(self.legs)].on_ground) and (self.legs[(i+1)%len(self.legs)].on_ground)
            leg.move([self.x,self.y],self.angle,tilemap,can_lift,
                     self.velocity,self.angular_velocity)
        self.weapon.gametick(deltatime)




