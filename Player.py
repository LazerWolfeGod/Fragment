import pygame


class Player:
    def __init__(self,ui,x,y):
        self.ui = ui
        self.x = x
        self.y = y
        self.keybinds = {'UP':[pygame.K_w,pygame.K_UP],
                         'DOWN':[pygame.K_s,pygame.K_DOWN],
                         'LEFT':[pygame.K_a,pygame.K_LEFT],
                         'RIGHT':[pygame.K_d,pygame.K_RIGHT],
                         'SHOOT':[pygame.K_SPACE]}
    def render_surf(self):
        radius = 15
        Surf = pygame.Surface((radius*2,radius*2),pygame.SRCALPHA)
        pygame.draw.circle(Surf,(150,100,60),(radius,radius),radius)
        return Surf

    def control(self):
        if self.get_pressed('UP'):
            self.y-=10*self.ui.deltatime
        if self.get_pressed('DOWN'):
            self.y+=10*self.ui.deltatime
        if self.get_pressed('LEFT'):
            self.x-=10*self.ui.deltatime
        if self.get_pressed('RIGHT'):
            self.x+=10*self.ui.deltatime

        if self.get_pressed('SHOOT'):
            self.shoot()

    def get_pressed(self,code):
        if code in self.keybinds:
            for k in self.keybinds[code]:
                if self.ui.kprs[k]:
                    return True
        return False

    def shoot(self):
        pass

    
        
