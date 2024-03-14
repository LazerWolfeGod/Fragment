import Map_Gen
import pygame
pygame.init()

from Utility_functions import *

class Data:
    # overlay string: n = not this tile, a = any tile, t = this tile
    
    tile = {0:{'File':'Assets\\Wall.png','Rect':[1,1,32,32],
               'Tile':{'atlas':[0,0],'hitbox':[(0,0,1,1)]},
               'overlays':{'atanaaan':{'atlas':[1,0,3],'hitbox':[(0,0,1,0.3)]},
                           'atatanan':{'atlas':[2,0,3],'hitbox':[(0,0,1,0.3),(0.7,0,0.3,1)]},
                           'aaantnaa':{'atlas':[0,1,3],'hitbox':[(0.7,0.7,0.3,0.3)]},
                           'atatatat':{'atlas':[1,1,0],'hitbox':[(0,0,1,0.3),(0,0,0.3,1),(0,0.7,1,0.3),(0.7,0,0.3,1)]},
                           'anatatat':{'atlas':[2,1,3],'hitbox':[(0,0,0.3,1),(0,0.7,1,0.3),(0.7,0,0.3,1)]}}},
            1:{'File':'Assets\\Tiles\\Cobble.png','Rect':[0,0,50,50],
               'Tile':{'atlas':[0,0],'hitbox':[]},'overlays':{}}}

    def process_overlays():
        def rotate_hitbox(hitbox):
            tl,tr,bl,br = (hitbox[0],hitbox[1]),(hitbox[0]+hitbox[2],hitbox[1]),(hitbox[0]+hitbox[2],hitbox[1]+hitbox[3]),(hitbox[0],hitbox[1]+hitbox[3])
            rotated = [(1-tl[1],tl[0]),(1-tr[1],tr[0]),(1-bl[1],bl[0]),(1-br[1],br[0])]
            topleft = (min([a[0] for a in rotated]),min([a[1] for a in rotated]))
            bottomright = (max([a[0] for a in rotated]),max([a[1] for a in rotated]))
            new_rec = (topleft[0],topleft[1],bottomright[0]-topleft[0],bottomright[1]-topleft[1])
            return new_rec
        
        for t in Data.tile:
            image = pygame.image.load(Data.tile[t]['File']).convert_alpha()
            rec = Data.tile[t]['Rect']
            image_grid = [[]]
            x = 0
            y = 0
            while True:
                image_grid[y].append(image.subsurface(pygame.Rect(rec[0]+x*(rec[0]+rec[2]),
                                                                  rec[1]+y*(rec[1]+rec[3]),
                                                                  rec[2],rec[3])))
                x+=1
                if rec[0]+x*(rec[0]+rec[2])>=image.get_width():
                    y+=1
                    if rec[1]+y*(rec[1]+rec[3])>=image.get_height():
                        break
                    image_grid.append([])
                    x = 0
            Data.tile[t]['Tile']['base_image'] = image_grid[Data.tile[t]['Tile']['atlas'][1]][Data.tile[t]['Tile']['atlas'][0]]
            new_overlays = {}
            for o in Data.tile[t]['overlays']:
                if Data.tile[t]['overlays'][o]['atlas']!=-1:
                    pos = Data.tile[t]['overlays'][o]['atlas']
                    hitbox = Data.tile[t]['overlays'][o]['hitbox'][:]
                    st = o
                    image = image_grid[pos[1]][pos[0]]
                    Data.tile[t]['overlays'][o]['base_image'] = image
                    for r in range(pos[2]):
                        image = pygame.transform.rotate(image,-90)
                        hitbox = [rotate_hitbox(a) for a in hitbox]
                        st = st[6:]+st[:6]
                        new_overlays[st] = {'base_image':image,
                                            'hitbox':hitbox,
                                            'atlas':-1}
            Data.tile[t]['overlays'].update(new_overlays)
                    
    
    def resize(scale,pixels=False):
        Data.process_overlays()
        for t in Data.tile:
            img = Data.tile[t]['Tile']['base_image']
            if not pixels: rec = (img.get_width()*scale,img.get_height()*scale)
            else: rec = (scale,scale)
            Data.tile[t]['Tile']['image'] = pygame.transform.scale(img,rec)
            for i in Data.tile[t]['overlays']:
                Data.tile[t]['overlays'][i]['image'] = pygame.transform.scale(Data.tile[t]['overlays'][i]['base_image'],rec)

Data.resize(1)

class Tile:
    def __init__(self,num,grid_x,grid_y,cell_size):
        self.num = num
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.cell_size = cell_size
        self.base_image = Data.tile[num]['Tile']['image'].copy()
        self.hitboxes = Data.tile[num]['Tile']['hitbox'][:]
    def get_image(self):
        return self.image
    def refresh(self,grid):
        overlay_list = []
        self.hitboxes = []
        search = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
        for offset in search:
            if pygame.Rect(0,0,len(grid[0]),len(grid)).collidepoint(self.grid_x+offset[0],self.grid_y+offset[1]):
                overlay_list.append(grid[self.grid_y+offset[1]][self.grid_x+offset[0]].num)
            else:
                overlay_list.append(-1)

        overlays = []
        for tile in Data.tile:
            if tile != self.num:
                for string in Data.tile[tile]['overlays']:
                    if self.compare_overlay_list(overlay_list,string,tile):
                        overlays.append(Data.tile[tile]['overlays'][string])
            


        relative_hitboxes = Data.tile[self.num]['Tile']['hitbox'][:]
        self.image = Data.tile[self.num]['Tile']['image'].copy()
        for overlay in overlays:
            relative_hitboxes+=overlay['hitbox']
            self.image.blit(overlay['image'],(0,0))

        self.hitboxes = []
        startx = self.grid_x*self.cell_size
        starty = self.grid_y*self.cell_size
        for hitbox in relative_hitboxes:
            self.hitboxes.append((startx+hitbox[0]*self.cell_size,
                                  starty+hitbox[1]*self.cell_size,
                                  hitbox[2]*self.cell_size,
                                  hitbox[3]*self.cell_size))
##            pygame.draw.rect(self.image,(255,0,0),pygame.Rect(hitbox[0]*self.cell_size,
##                                                              hitbox[1]*self.cell_size,
##                                                              hitbox[2]*self.cell_size,
##                                                              hitbox[3]*self.cell_size))
            
            
    def compare_overlay_list(self,overlay_list,overlay_string,tile):
        for i in range(len(overlay_list)):
            if overlay_string[i] != 'a':
                if overlay_string[i] == 't' and overlay_list[i] != tile:
                    return False
                elif overlay_string[i] == 'n' and overlay_list[i] == tile:
                    return False
        return True
        
        
    def get_collide(self,hitbox):
        if type(hitbox) == list:
            return list_list_collide(self.hitboxes,hitbox)
        else:
            return list_obj_collide(self.hitboxes,hitbox)
    
class TileMap:
    def __init__(self,grid,cell_size):
        # 0 = wall tile
        # 1 = floor tile
        # . 
        #
        self.tiles = {1:{'File':'Assets\\Tilemap.png','Spacing':[1,1,32,32],'tilekey':
                               {'........':[0,0],
                                '*1*0*0*0':[0,1],'*0*1*0*0':[1,1],'*0*0*1*0':[2,1],'*0*0*0*1':[3,1],
                                '*1*1*0*0':[0,2],'*0*1*1*0':[1,2],'*0*0*1*1':[2,2],'*1*0*0*1':[3,2],
                                '*010*0*0':[0,3],'*0*010*0':[1,3],'*0*0*010':[2,3],'10*0*0*0':[3,3]}}}

        self.grid_h = len(grid)
        self.grid_w = len(grid[0])
        self.cell_size = cell_size
        
        self.grid = []
        for y in range(self.grid_h):
            self.grid.append([])
            for x in range(self.grid_w):
                self.grid[-1].append(Tile(grid[y][x],x,y,self.cell_size))
        self.refresh()

        self.marked_hitbox = []
        
    def render(self,Surf):
        for y in range(self.grid_h):
            for x in range(self.grid_w):
                Surf.blit(self.grid[y][x].get_image(),(x*self.cell_size,y*self.cell_size))
        return Surf
    def refresh(self):
        for y in self.grid:
            for x in y:
                x.refresh(self.grid)
                
    def check_collisions(self,obj):
        if len(obj) == 3:
            top_left = self.world_pos_to_grid_pos((obj[0]-obj[2],obj[1]-obj[2]))
            bottom_right = self.world_pos_to_grid_pos((obj[0]+obj[2],obj[1]+obj[2]))
        else:
            top_left = self.world_pos_to_grid_pos((obj[0],obj[1]))
            bottom_right = self.world_pos_to_grid_pos((obj[0]+obj[2],obj[1]+obj[3]))
        
        for y in range(top_left[1]-1,bottom_right[1]+2):
            for x in range(top_left[0]-1,bottom_right[0]+2):
                if self.grid[y][x].get_collide(obj):
                    return True
        return False
    def world_pos_to_grid_pos(self,pos):
        grid_pos = [int(pos[0]//self.cell_size),int(pos[1]//self.cell_size)]
        return grid_pos
    def check_in_grid(self,grid_pos):
        return grid_pos[0]>-1 and grid_pos[1]>-1 and grid_pos[0]<self.grid_w and grid_pos[1]<self.grid_h  
        
    def get_width(self):
        return self.grid_w
    def get_height(self):
        return self.grid_h
        

class Map:
    def __init__(self,cell_size=32):
        Data.resize(cell_size,True)
        self.cell_size = cell_size
        
        grid = [[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,1,1,1,1,1,0,0],
                [0,1,1,1,1,0,1,0,1,1,1,0,0,0,1,0,1,1,1,1,1,0,0],
                [0,1,0,1,0,1,1,0,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0],
                [0,1,1,1,0,1,1,1,1,0,0,1,0,0,0,0,1,1,1,1,1,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0],
                [0,1,1,1,0,0,1,1,1,0,1,1,1,1,0,0,0,0,0,0,1,0,0],
                [0,1,0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0],
                [0,1,1,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        self.tilemap = TileMap(grid,cell_size)
        
    def render_surf(self):
        Surf = pygame.Surface((self.tilemap.grid_w*self.cell_size,
                               self.tilemap.grid_h*self.cell_size))
        Surf = self.tilemap.render(Surf)

        return Surf






    
