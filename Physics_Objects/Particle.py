import math,pygame,random
from Physics_Objects.Physics_Object import Abstract_Physics_Object
from Physics_Objects.Physics_Object_Data import Data


class Particle(Abstract_Physics_Object):
    def __init__(self,ui,x,y,speed,angle,name):
        self.name = name
        stats = Data.particles[self.name]['Stats']
        super().__init__(ui,x,y,speed,angle,stats)

        self.image = Data.particles[self.name]['Image']

        self.base_image = pygame.transform.scale(self.image,(self.image.get_width()*(self.radius*2/self.image.get_height()),stats['Width']))
        self.image = pygame.transform.rotate(self.base_image,-angle/math.pi*180)

class Spark(Particle):
    def __init__(self,ui,x,y,speed,angle):
        super().__init__(ui,x,y,speed,angle,'Spark')
    def child_gametick(self,_):
        self.alpha = int(255*(self.get_speed()/self.initial_speed))
    def check_finished(self):
        return self.alpha < 40

class Laser_Dust(Particle):
    def __init__(self,ui,x,y,speed,angle):
        super().__init__(ui,x,y,speed,angle,'Laser_Dust')
    def child_gametick(self,_):
        self.alpha = int(150*(self.get_speed()/self.initial_speed))
    def check_finished(self):
        return self.alpha < 40
        


