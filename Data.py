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
            1:{'File':'Assets\\Tiles\\Metal.png','Rect':[0,0,100,100],
               'Tile':{'atlas':[0,0],'hitbox':[]},'overlays':{}}}


    def process_tile_overlays():
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
                    
    
    def resize_tiles(scale,pixels=False):
        Data.process_tile_overlays()
        for t in Data.tile:
            img = Data.tile[t]['Tile']['base_image']
            if not pixels: rec = (img.get_width()*scale,img.get_height()*scale)
            else: rec = (scale,scale)
            Data.tile[t]['Tile']['image'] = pygame.transform.scale(img,rec)
            for i in Data.tile[t]['overlays']:
                Data.tile[t]['overlays'][i]['image'] = pygame.transform.scale(Data.tile[t]['overlays'][i]['base_image'],rec)


Data.resize_tiles(1)

