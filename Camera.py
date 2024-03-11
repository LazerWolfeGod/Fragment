import pygame

class Camera:
    def __init__(self,target):
        self.target = target
        self.x = target.x
        self.y = target.y
        self.zoom = 1
    def render(self,disp_w,disp_h):
        Surf = pygame.Surface((disp_w,disp_h))
        
        target_surf = self.target.render()

    def transform(self,x,y):
        
        
        
