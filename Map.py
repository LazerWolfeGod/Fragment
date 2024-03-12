import Map_Gen
import pygame
pygame.init()

from Utility_functions import *

class Data:
    # overlay string: n = not this tile, a = any tile, t = this tile
    
    tile = {0:{'File':'Assets\\Wall.png','Rect':[1,1,32,32],
               'Tile':[0,0],'overlays':{'atanaaan':[1,0,3],
                                        'atatanan':[2,0,3],
                                        'aaantnaa':[0,1,3],
                                        'atatatat':[1,1,0],
                                        'anatatat':[2,1,3]}},
            1:{'File':'Assets\\Tiles\\Cobble.png','Rect':[0,0,50,50],
               'Tile':[0,0],'overlays':{}}}

    def process_overlays():
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
            Data.tile[t]['image_map'] = {}
            Data.tile[t]['image'] = image_grid[Data.tile[t]['Tile'][1]][Data.tile[t]['Tile'][0]]
            for o in Data.tile[t]['overlays']:
                pos = Data.tile[t]['overlays'][o]
                st = o
                image = image_grid[pos[1]][pos[0]]
                Data.tile[t]['image_map'][o] = image
                for r in range(pos[2]):
                    image = pygame.transform.rotate(image,-90)
                    st = st[6:]+st[:6]
                    Data.tile[t]['image_map'][st] = image
                    
    
    def resize(scale,pixels=False):
        Data.process_overlays()
        for t in Data.tile:
            img = Data.tile[t]['image']
            if not pixels: rec = (img.get_width()*scale,img.get_height()*scale)
            else: rec = (scale,scale)
            Data.tile[t]['image'] = pygame.transform.scale(img,rec)
            for i in Data.tile[t]['image_map']:
                Data.tile[t]['image_map'][i] = pygame.transform.scale(Data.tile[t]['image_map'][i],rec)

Data.resize(1)

class Tile:
    def __init__(self,num,grid_x,grid_y):
        self.num = num
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.base_image = Data.tile[num]['image'].copy()
    def get_image(self):
        return self.image
    def refresh_image(self,grid):
        overlay_list = []
        search = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
        for offset in search:
            if pygame.Rect(0,0,len(grid[0]),len(grid)).collidepoint(self.grid_x+offset[0],self.grid_y+offset[1]):
                overlay_list.append(grid[self.grid_y+offset[1]][self.grid_x+offset[0]].num)
            else:
                overlay_list.append(-1)

        layered_surfaces = []
        for tile in Data.tile:
            if tile != self.num:
                for string in Data.tile[tile]['image_map']:
                    if self.compare_overlay_list(overlay_list,string,tile):
                        layered_surfaces.append(Data.tile[tile]['image_map'][string])
                        
        self.image = self.base_image.copy()
        for surf in layered_surfaces:
            self.image.blit(surf,(0,0))
                
            
    def compare_overlay_list(self,overlay_list,overlay_string,tile):
        for i in range(len(overlay_list)):
            if overlay_string[i] != 'a':
                if overlay_string[i] == 't' and overlay_list[i] != tile:
                    return False
                elif overlay_string[i] == 'n' and overlay_list[i] == tile:
                    return False
        return True
        
        
    def get_collide(self):
        pass
    
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
                self.grid[-1].append(Tile(grid[y][x],x,y))
        self.refresh()
        
    def render(self,Surf):
        for y in range(self.grid_h):
            for x in range(self.grid_w):
                Surf.blit(self.grid[y][x].get_image(),(x*self.cell_size,y*self.cell_size))
        return Surf
    def refresh(self):
        for y in self.grid:
            for x in y:
                x.refresh_image(self.grid)

    def get_width(self):
        return self.grid_w
    def get_height(self):
        return self.grid_h
        

class Map:
    def __init__(self,cell_size=32):
        Data.resize(cell_size,True)
        self.cell_size = cell_size
        
        grid = [[0,0,0,0,0,0,0,0,1],
                [0,1,1,0,1,1,1,0,0],
                [0,1,1,1,1,0,1,0,1],
                [0,1,1,0,0,1,1,0,1],
                [0,1,1,0,0,1,1,1,1],
                [0,0,0,0,0,0,0,0,0]]
        self.tilemap = TileMap(grid,cell_size)
        
    def render_surf(self):
        Surf = pygame.Surface((self.tilemap.grid_w*self.cell_size,
                               self.tilemap.grid_h*self.cell_size))
        Surf = self.tilemap.render(Surf)

        return Surf






    
