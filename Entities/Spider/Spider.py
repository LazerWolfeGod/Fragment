import pygame,math,random
from Utility_functions import *
from Entities.Spider.Spider_Data import Data
from Entities.Spider.Leg import Leg
from Entities.Spider.Body import Body
from Entities.Spider.Weapon import Weapon
from Entities.Entity import Entity

class Spider(Entity):
    def __init__(self,ui,x,y,leg_name,body_name,weapon_name):
        super().__init__(ui,x,y)
        self.thing = 'Spider'
        self.target_angle = 0
        
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

        self.health = self.body.health
        self.defence = 0
        self.mass = self.body.mass

        
    def make_legs(self):
        self.num_legs = Data.Legs[self.leg_name]['Stats']['Num_Legs']
        self.legs = [Leg([self.x,self.y],self.angle,(theta/self.num_legs*math.tau-math.pi+math.pi/self.num_legs),
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

    def shoot(self,projectiles):
        kickback = self.weapon.shoot(projectiles,self.ui,self.x,self.y,self.angle,self.velocity,self.team)

        self.velocity[0]-=kickback*math.cos(self.angle)/self.mass
        self.velocity[1]-=kickback*math.sin(self.angle)/self.mass


    def gametick(self,mapp,projectiles,entities,deltatime):
        self.control(mapp,projectiles,entities)
        self.move(mapp,deltatime)
        self.spider_physics(deltatime)
        
    def child_move(self,mapp,deltatime):
        if self.move_vector.magnitude()>0: self.move_vector.normalize_ip()
        self.move_vector*=(5+math.cos(self.angle-self.move_vector.as_polar()[1]/180*math.pi))/6
        self.move_vector*=self.move_acceleration*self.ui.deltatime

        self.velocity+=self.move_vector

        if (self.angle-self.target_angle)%math.tau<(self.target_angle-self.angle)%math.tau:
            self.angular_velocity-=min(self.turn_acceleration,(self.angle-self.target_angle)%math.tau)
        else:
            self.angular_velocity+=min(self.turn_acceleration,(self.target_angle-self.angle)%math.tau)
            

    def spider_physics(self,deltatime):
        for i,leg in enumerate(self.legs):
            on_ground = [l.on_ground for l in self.legs]
            can_lift = sum(on_ground)>int(len(self.legs)/2) and (self.legs[(i-1)%len(self.legs)].on_ground) and (self.legs[(i+1)%len(self.legs)].on_ground)
            leg.move(deltatime,[self.x,self.y],self.angle,can_lift,
                     self.velocity,self.angular_velocity)
        self.weapon.gametick(deltatime)

    def control(self,**_): pass



