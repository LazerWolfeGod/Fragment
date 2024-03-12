import pygame

class Camera:
    def __init__(self,target,display_rect):
        self.display_rect = display_rect
        self.target = target
        self.x = self.target.x
        self.y = self.target.y
        self.zoom = 1
        
        self.velocity = [0,0]
        self.acceleration_constant = 0.01
        
    def render(self,screen,mapp,players):
        Surf = pygame.Surface((self.display_rect.w,self.display_rect.h))
        Surf.fill((40,40,40))

        map_surf = mapp.render_surf()
        Surf.blit(map_surf,self.transform(0,0))

        for p in players:
            player_surf = p.render_surf()
            Surf.blit(player_surf,self.transform(p.x-player_surf.get_width(),
                                                 p.y-player_surf.get_height()))

        screen.blit(Surf,self.display_rect.topleft)
        

    def transform(self,x=0,y=0,return_tuple=True):
        if not type(x) in [list,tuple]: pos = [x,y]
        else: pos = x
        ret = (pos[0]-self.x+self.display_rect.w/2,pos[1]-self.y+self.display_rect.h/2)
        
        if return_tuple:
            return ret
        else:
            return ret[0],ret[1]

    def move(self):
        self.velocity[0]+=self.acceleration_constant*(self.target.x-self.x)
        self.velocity[1]+=self.acceleration_constant*(self.target.y-self.y)

        self.x+=self.velocity[0]
        self.y+=self.velocity[1]

        damping = (30*self.acceleration_constant)**0.5
        self.velocity[0]*=damping
        self.velocity[1]*=damping



##        self.x = self.target.x
##        self.y = self.target.y






        
