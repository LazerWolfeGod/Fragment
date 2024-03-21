import math,pygame,random
from Physics_Objects.Physics_Object_Data import Data


class Abstract_Physics_Object:
    def __init__(self,ui,x,y,speed,angle,stats):
        self.ui = ui
        self.x = x
        self.y = y
        self.initial_speed = abs(speed)
        self.velocity = pygame.Vector2([speed*math.cos(angle),speed*math.sin(angle)])
        self.angle = angle
        self.lifetime = 300
        self.alpha = 255
        
        self.finished = False

        d_copy = Data.physics_defaults.copy()
        d_copy.update(stats)
        stats = d_copy
        
        self.restitution = stats['Restitution']
        self.collision_count = stats['Collision_Limit']
        self.has_collisions = stats['Has_Collisions']
        self.drag = stats['Drag']
        self.width = stats['Width']
        if type(self.width) in [list,tuple]:
            self.width = max(random.gauss(self.width[0],self.width[1]),1)
        self.radius = self.width/2
        
        
    def move(self,tilemap,particles):
        self.child_gametick(particles)

        self.lifetime-=self.ui.deltatime

        self.velocity[0]*=self.drag
        self.velocity[1]*=self.drag
        
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
        self.collision_count-=1
        if self.collision_count<0:
            self.finished = True
        self.child_on_collision()
        
    def render_surf(self):
        self.image.set_alpha(int(self.alpha))
        return self.image

    def get_speed(self):
        return (self.velocity[0]**2+self.velocity[1]**2)**0.5
    def get_angle(self):
        return math.atan2(self.velocity[1],self.velocity[0])

    def check_tilemap_collision(self,tilemap):
        if self.has_collisions:
            self.hitbox = (self.x,self.y,self.radius)
            return tilemap.check_collisions(self.hitbox)
        return False

    def check_finished(self):
        return self.lifetime<0 or self.alpha == 0 or self.finished

    def child_on_collision(self): pass
    def child_gametick(self,_): pass
    def finish(self,_): pass


