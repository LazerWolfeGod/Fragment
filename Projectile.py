
class Projectile:
    def __init__(self,ui,x,y,radius,vel):
        self.ui = ui
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = vel
        self.lifetime = 0
    def move(self):
        self.lifetime+=self.ui.deltatime/60
        self.x+=self.vel[0]
        self.y+=self.vel[1]

    def render_surf(self):
        Surf = pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA)
        pygame.draw.circle(Surf,(150,60,100),(self.radius,self.radius),self.radius)
        return Surf
        
    
