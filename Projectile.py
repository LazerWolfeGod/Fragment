import math,pygame,random
from Physics_Objects.Physics_Object import Abstract_Physics_Object
from Physics_Objects.Particle import *
from Physics_Objects.Physics_Object_Data import Data

class Projectile(Abstract_Physics_Object):
    def __init__(self,ui,x,y,speed,angle,name):
        self.name = name
        stats = Data.projectiles[self.name]['Stats']
        super().__init__(ui,x,y,speed,angle,stats)
        
        self.image = Data.projectiles[self.name]['Image']
        self.base_image = pygame.transform.scale(self.image,(self.image.get_width()*(stats['Width']/self.image.get_height()),stats['Width']))
        self.image = pygame.transform.rotate(self.base_image,-angle/math.pi*180)
        
    
class Fader(Projectile):
    def __init__(self,ui,x,y,angle,speed=8):
        super().__init__(ui,x,y,speed)
    def child_gametick(self,_):
        self.radius*=self.energyloss

    def check_finished(self):
        return self.radius<1

class Energy_Ball(Projectile):
    def __init__(self,ui,x,y,angle,speed=12):
        super().__init__(ui,x,y,speed,angle,'Energy_Ball')

class Bullet(Projectile):
    def __init__(self,ui,x,y,angle,speed=12):
        super().__init__(ui,x,y,speed,angle,'Bullet')

class Fire(Projectile):
    def __init__(self,ui,x,y,angle,speed=12):
        super().__init__(ui,x,y,speed,angle,'Fire')
        self.initial_speed = speed
    def check_finished(self):
        return self.alpha < 40 or self.finished
    def child_gametick(self,particles):
        particles.append(Spark(self.ui,self.x,self.y,random.gauss(self.get_speed(),1)*0.7,
                               self.get_angle()-math.pi+random.gauss(0,0.05)))
        particles[-1].initial_speed = self.initial_speed
        self.alpha = int(255*(self.get_speed()/self.initial_speed))
        
    
