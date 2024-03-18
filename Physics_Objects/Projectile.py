import math,pygame,random
from Particles import Abstract_Physics_Object
from Data import Data

class Projectile(Abstract_Physics_Object):
    def __init__(self,ui,x,y,speed,angle,name):
        super().__init__(ui,x,y,speed,angle)
        
        self.name = name
        self.image = Data.projectiles[self.name]['Image']
        stats = Data.projectiles[self.name]['Stats']
        self.base_image = pygame.transform.scale(self.image,(self.image.get_width()*(stats['Width']/self.image.get_height()),stats['Width']))
        self.image = pygame.transform.rotate(self.base_image,-angle/math.pi*180)
        self.radius = stats['Width']/2
        
    
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
    def __init__(self,ui,x,y,angle,speed=12):
        super().__init__(ui,x,y,speed,angle,'Energy_Ball')
    def child_on_collision(self):
        self.finished = True

class Bullet(Projectile):
    def __init__(self,ui,x,y,angle,speed=12):
        super().__init__(ui,x,y,speed,angle,'Bullet')
    def child_on_collision(self):
        self.finished = True

class Fire(Projectile):
    def __init__(self,ui,x,y,angle,speed=12):
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
    def child_gametick(self):
        self.alpha = int(255*(self.velocity[0]**2+self.velocity[1]**2)**0.5/self.initial_speed)
        
    
