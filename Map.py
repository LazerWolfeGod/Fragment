import Map_Gen
import pygame
pygame.init()

from Utility_functions import *

class Assets:
    tiles = {0:pygame.image.load('Assets\\Tiles\\Wall.png').convert_alpha(),
             1:pygame.image.load('Assets\\Tiles\\Floor.png').convert_alpha()}

class Tile:
    def __init__(self,num):
        self.image = Assets.tiles[num]
    def get_image(self):
        return self.image
    
class TileMap:
    def __init__(self,grid):
        # 1 = floor tile
        # 0 = wall tile
        # . 
        #
        self.tiles = {1:{'File':'Assets\\Tilemap.png','Spacing':[1,1,32,32],'tilekey':
                               {'........':[0,0],
                                '*1*0*0*0':[0,1],'*0*1*0*0':[1,1],'*0*0*1*0':[2,1],'*0*0*0*1':[3,1],
                                '*1*1*0*0':[0,2],'*0*1*1*0':[1,2],'*0*0*1*1':[2,2],'*1*0*0*1':[3,2],
                                '*010*0*0':[0,3],'*0*010*0':[1,3],'*0*0*010':[2,3],'10*0*0*0':[3,3]}}}

        self.grid_h = len(grid)
        self.grid_w = len(grid[0])
        
        self.grid = []
        for y in range(len(grid)):
            self.grid.append([])
            for x in range(len(grid[y])):
                self.grid[-1].append(Tile(grid[y][x]))
    def render(self,Surf,cell_size):
        for y in range(self.grid_h):
            for x in range(self.grid_w):
                Surf.blit(self.grid[y][x].get_image(),(x*cell_size,y*cell_size))
                

    def get_width(self):
        return self.grid_w
    def get_height(self):
        return self.grid_h
        

class Map:
    def __init__(self,cell_size=32):
        self.cell_size = cell_size
        
        grid = [[0,0,0,0,0,0,0,0],
                [0,1,1,0,1,1,1,0],
                [0,1,1,1,1,0,1,0],
                [0,1,1,0,0,1,1,0],
                [0,1,1,0,0,1,1,0],
                [0,0,0,0,0,0,0,0]]
        self.tilemap = TileMap(grid)
        
    def render(self):
        Surf = pygame.Surface((self.tilemap.get_width*self.cell_size,
                               self.tilemap.get_height*self.cell_size))
        Surf = self.tilemap.Render(Surf)






    
