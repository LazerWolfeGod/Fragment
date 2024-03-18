import pygame

class Camera:
    def __init__(self,target,display_rect):
        self.display_rect = display_rect
        self.target = target
        self.x = self.target.x
        self.y = self.target.y
        self.zoom = 1
        
        self.velocity = [0,0]
        self.acceleration_constant = 0.03
        
    def render(self,screen,mapp,players,projectiles,particles):
        Surf = pygame.Surface((self.display_rect.w,self.display_rect.h))
        Surf.fill((40,40,40))

        map_surf = mapp.render_surf()
        Surf.blit(map_surf,self.transform(0,0))

        for p in particles:
            proj_surf = p.render_surf()
            Surf.blit(proj_surf,self.transform(p.x-proj_surf.get_width()/2,
                                               p.y-proj_surf.get_height()/2))

            
        for p in projectiles:
            proj_surf = p.render_surf()
            Surf.blit(proj_surf,self.transform(p.x-proj_surf.get_width()/2,
                                               p.y-proj_surf.get_height()/2))


        for p in players:
            player_surf = p.render_surf()
            Surf.blit(player_surf,self.transform(p.x-player_surf.get_width()/2,
                                                 p.y-player_surf.get_height()/2))
            p.mpos = self.screen_pos_to_world_pos(self.target.ui.mpos)
        

        screen.blit(Surf,self.display_rect.topleft)
        

    def transform(self,x=0,y=0,return_tuple=True):
        if not type(x) in [list,tuple]: pos = [x,y]
        else: pos = x
        ret = (pos[0]-self.x+self.display_rect.w/2,pos[1]-self.y+self.display_rect.h/2)
        
        if return_tuple:
            return ret
        else:
            return ret[0],ret[1]
    def screen_pos_to_world_pos(self,pos):
        return [pos[0]-self.display_rect.x+self.x-self.display_rect.w/2,
                pos[1]-self.display_rect.y+self.y-self.display_rect.h/2]

    def move(self):
        self.velocity[0]+=self.acceleration_constant*(self.target.x-self.x)
        self.velocity[1]+=self.acceleration_constant*(self.target.y-self.y)

        self.x+=self.velocity[0]
        self.y+=self.velocity[1]

        damping = 0.84-4*self.acceleration_constant
        
        self.velocity[0]*=damping
        self.velocity[1]*=damping



##        self.x = self.target.x
##        self.y = self.target.y






        
