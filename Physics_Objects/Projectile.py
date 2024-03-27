import math,pygame,random
from Physics_Objects.Particle import *
from Physics_Objects.Physics_Object import Abstract_Physics_Object
from Physics_Objects.Physics_Object_Data import Data
from Utility_functions import *

class Projectile(Abstract_Physics_Object):
    def __init__(self,ui,x,y,speed,angle,team,damage,name):
        self.name = name
        self.team = team
        stats = Data.projectiles[self.name]['Stats']
        super().__init__(ui,x,y,speed,angle,stats)
        self.thing = 'Projectile'
        
        self.image = Data.projectiles[self.name]['Image']

        self.length = self.image.get_width()*(self.width/self.image.get_height())
        self.base_image = pygame.transform.scale(self.image,(self.length,self.width))
        self.image = pygame.transform.rotate(self.base_image,-angle/math.pi*180)

        self.damage = damage
        self.knockback = stats['Knockback']
##    def check_entity_collide(self,entities):
##        for e in entities:
##            if e.team!=self.team:
##                if e.get_collide((self.x,self.y,self.radius)):
##                    e.take_damage(self.damage,self.velocity,self.knockback)
##                    self.collide()
    def collide_object(self,obj):
        obj.take_damage(self.damage*(self.get_speed()/self.initial_speed),self.velocity,self.knockback)
            

class Energy_Ball(Projectile):
    def __init__(self,ui,x,y,angle,speed,team,damage):
        super().__init__(ui,x,y,speed,angle,team,damage,'Energy_Ball')

class Bullet(Projectile):
    def __init__(self,ui,x,y,angle,speed,team,damage):
        super().__init__(ui,x,y,speed,angle,team,damage,'Bullet')
    def finish(self,particles):
        for a in range(20):
            particles.append(Dust(self.ui,self.x,self.y,
                                  random.gauss(self.velocity.magnitude(),2),
                                  random.gauss(self.angle,0.5)))

class Fire(Projectile):
    def __init__(self,ui,x,y,angle,speed,team,damage):
        super().__init__(ui,x,y,speed,angle,team,damage,'Fire')
        self.initial_speed = speed
        self.alpha = 255
    def render_surf(self):
        self.image.set_alpha(self.alpha)
        return self.image
    def check_finished(self):
        return self.alpha<10 or self.finished
    def child_gametick(self,particles):
        particles.append(Spark(self.ui,self.x,self.y,random.gauss(self.get_speed(),1)*0.7,
                               self.get_angle()-math.pi+random.gauss(0,0.05)))
        particles[-1].initial_speed = self.initial_speed
        self.alpha = int(255*(self.get_speed()/self.initial_speed))

class Laser(Projectile):
    def __init__(self,ui,x,y,angle,speed,team,damage):
        super().__init__(ui,x,y,speed,angle,team,damage,'Laser')
    def child_gametick(self,particles):
        pos = (random.random()-0.5)*self.length
        particles.append(Laser_Dust(self.ui,self.x+math.cos(self.angle)*pos,self.y+math.sin(self.angle)*pos,
                                    random.gauss(0,1),random.gauss(0,math.pi)))
    def finish(self,particles):
        for a in range(10):
            pass

class Pellet(Projectile):
    def __init__(self,ui,x,y,angle,speed,team,damage):
        super().__init__(ui,x,y,speed,angle,team,damage,'Pellet')
        self.constant_vel = random.gauss(40,10)
    def child_gametick(self,particles):
        self.alpha = int(255*(self.get_speed()/self.initial_speed))

class Wave(Projectile):
    def __init__(self,ui,x,y,angle,speed,team,damage):
        super().__init__(ui,x,y,speed,angle,team,damage,'Wave')
        self.constant_vel = 16
    def child_gametick(self,particles):
        self.alpha = int(255*(self.get_speed()/self.initial_speed))

class Melee(Projectile):
    def __init__(self,ui,x,y,angle,speed,team,damage):
        super().__init__(ui,x,y,speed,angle,team,damage,'Melee')

    
