import math,pygame,random

class Projectile:
    def __init__(self,ui,x,y,radius,velocity,resistivity=0.5):
        self.ui = ui
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = velocity
        self.lifetime = random.gauss(600,100)
        self.resistivity = resistivity
        self.collision_count = 0
    def move(self,tilemap):
        self.child_gametick()

        self.lifetime-=self.ui.deltatime
        
        self.lifetime+=self.ui.deltatime/60
        self.x+=self.velocity[0]
        if self.check_tilemap_collision(tilemap):
            self.x-=self.velocity[0]
            self.velocity[0]*=-self.resistivity
            self.child_on_collision()
        self.y+=self.velocity[1]
        if self.check_tilemap_collision(tilemap):
            self.y-=self.velocity[1]
            self.velocity[1]*=-self.resistivity
            self.child_on_collision()


    def render_surf(self):
        Surf = pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA)
        pygame.draw.circle(Surf,(60,60,60),(self.radius,self.radius),self.radius)
        return Surf

    def check_tilemap_collision(self,tilemap):
        self.hitbox = (self.x,self.y,self.radius)
        return tilemap.check_collisions(self.hitbox)

    def check_finished(self):
        return self.lifetime<0
    def child_gametick(self): pass
    def child_on_collision(self): pass
    
class Fader(Projectile):
    def __init__(self,ui,x,y,angle,speed=8,energyloss=0.98):
        super().__init__(ui,x,y,5+random.gauss(0,0.5),[speed*math.cos(angle),speed*math.sin(angle)])
        self.energyloss = energyloss
    def child_gametick(self):
        self.velocity[0]*=self.energyloss
        self.velocity[1]*=self.energyloss

        self.radius*=self.energyloss

    def check_finished(self):
        return self.radius<1

class Energy_Ball(Projectile):
    def __init__(self,ui,x,y,angle,speed=12):
        super().__init__(ui,x,y,5+random.gauss(0,0.5),[speed*math.cos(angle),speed*math.sin(angle)])
        self.finished = False
        
    def check_finished(self):
        return self.finished
    def child_on_collision(self):
        self.finished = True

class Bullet(Projectile):
    def __init__(self,ui,x,y,angle,speed=12):
        super().__init__(ui,x,y,5+random.gauss(0,0.2),[speed*math.cos(angle),speed*math.sin(angle)])
        self.finished = False
        
    def check_finished(self):
        return self.finished
    def child_on_collision(self):
        self.finished = True
    
