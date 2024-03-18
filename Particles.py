import math,pygame,random
from Data import Data


class Physics_Object:
    def __init__(self,ui,x,y,speed,angle):
        self.ui = ui
        self.x = x
        self.y = y
        self.velocity = [speed*math.cos(angle),speed*math.sin(angle)]
        self.angle = angle
        self.lifetime = random.gauss(600,100)
        
        self.collision_count = 0
        self.finished = False
        
        
    def move(self,tilemap):
        self.child_gametick()

        self.lifetime-=self.ui.deltatime
        
        self.x+=self.velocity[0]
        if self.check_tilemap_collision(tilemap):
            self.x-=self.velocity[0]
            self.velocity[0]*=-self.restitution
            self.collide()
        self.y+=self.velocity[1]
        if self.check_tilemap_collision(tilemap):
            self.y-=self.velocity[1]
            self.velocity[1]*=-self.restitution
            self.collide()
            

    def collide(self):
        angle = math.atan2(self.velocity[1],self.velocity[0])
        self.image = pygame.transform.rotate(self.base_image,-angle/math.pi*180)
        self.child_on_collision()
        
    def render_surf(self):
        return self.image

    def check_tilemap_collision(self,tilemap):
        self.hitbox = (self.x,self.y,self.radius)
        return tilemap.check_collisions(self.hitbox)

    def check_finished(self):
        return self.lifetime<0 or self.finished

    def child_on_collision(self): pass
    def child_gametick(self): pass


