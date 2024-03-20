import math,pygame,random
from Physics_Objects.Particle import *
from Physics_Objects.Physics_Object import Abstract_Physics_Object
from Physics_Objects.Physics_Object_Data import Data

class Projectile(Abstract_Physics_Object):
    def __init__(self,ui,x,y,speed,angle,name):
        self.name = name
        stats = Data.projectiles[self.name]['Stats']
        super().__init__(ui,x,y,speed,angle,stats)
        
        self.image = Data.projectiles[self.name]['Image']

        self.length = self.image.get_width()*(stats['Width']/self.image.get_height())
        self.base_image = pygame.transform.scale(self.image,(self.length,stats['Width']))
        self.image = pygame.transform.rotate(self.base_image,-angle/math.pi*180)

    
    
class Fader(Projectile):
    def __init__(self,ui,x,y,angle,speed=8,energyloss=0.98):
        super().__init__(ui,x,y,speed)
        self.energyloss = energyloss
    def child_gametick(self):
        self.velocity[0]*=self.energyloss
        self.velocity[1]*=self.energyloss

        self.radius*=self.energyloss

    def check_finished(self):
        return self.radius<1

class Energy_Ball(Projectile):
    def __init__(self,ui,x,y,angle,speed):
        super().__init__(ui,x,y,speed,angle,'Energy_Ball')
    def child_on_collision(self):
        self.finished = True

class Bullet(Projectile):
    def __init__(self,ui,x,y,angle,speed):
        super().__init__(ui,x,y,speed,angle,'Bullet')
    def child_on_collision(self):
        self.finished = True

class Fire(Projectile):
    def __init__(self,ui,x,y,angle,speed):
        super().__init__(ui,x,y,speed,angle,'Fire')
        self.initial_speed = speed
        self.alpha = 255
    def render_surf(self):
        self.image.set_alpha(self.alpha)
        return self.image
    def child_collision(self):
        self.finished = True
    def check_finished(self):
        return self.alpha<10 or self.finished
    def child_gametick(self,particles):
        particles.append(Spark(self.ui,self.x,self.y,random.gauss(self.get_speed(),1)*0.7,
                               self.get_angle()-math.pi+random.gauss(0,0.05)))
        particles[-1].initial_speed = self.initial_speed
        self.alpha = int(255*(self.get_speed()/self.initial_speed))

class Laser(Projectile):
    def __init__(self,ui,x,y,angle,speed):
        super().__init__(ui,x,y,speed,angle,'Laser')
    def child_gametick(self,particles):
        pos = (random.random()-0.5)*self.length
        particles.append(Laser_Dust(self.ui,self.x+math.cos(self.angle)*pos,self.y+math.sin(self.angle)*pos,
                                    random.gauss(0,1),random.gauss(0,math.pi)))
        
