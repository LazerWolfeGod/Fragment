import pygame
pygame.init()

from Utility_functions import *

class Data:
    # overlay string: n = not this tile, a = any tile, t = this tile
    
    tile = {'None':{'File':'Assets\\Tiles\\Blank_Tile.png','Rect':[0,0,100,100],
                    'Tile':{'atlas':[0,0],'hitbox':[]},'Layer':-100,'overlays':{}},
            'Black_Wall':{'File':'Assets\\Tiles\\Wall.png','Rect':[1,1,32,32],
               'Tile':{'atlas':[0,0],'hitbox':[(0,0,1,1)]},'Layer':100,
               'overlays':{'atanaaan':{'atlas':[1,0,3],'hitbox':[(0,0,1,0.3)]},
                           'atatanan':{'atlas':[2,0,3],'hitbox':[(0,0,1,0.3),(0.7,0,0.3,1)]},
                           'aaantnaa':{'atlas':[0,1,3],'hitbox':[(0.7,0.7,0.3,0.3)]},
                           'atatatat':{'atlas':[1,1,0],'hitbox':[(0,0,1,0.3),(0,0,0.3,1),(0,0.7,1,0.3),(0.7,0,0.3,1)]},
                           'anatatat':{'atlas':[2,1,3],'hitbox':[(0,0,0.3,1),(0,0.7,1,0.3),(0.7,0,0.3,1)]}}},
            'Black_Wall_Thinner':{'File':'Assets\\Tiles\\Wall_Thinner.png','Rect':[1,1,32,32],
               'Tile':{'atlas':[0,0],'hitbox':[(0,0,1,1)]},'Layer':99,
               'overlays':{'atanaaan':{'atlas':[1,0,3],'hitbox':[(0,0,1,0.2)]},
                           'atatanan':{'atlas':[2,0,3],'hitbox':[(0,0,1,0.2),(0.8,0,0.2,1)]},
                           'aaantnaa':{'atlas':[0,1,3],'hitbox':[(0.8,0.8,0.2,0.2)]},
                           'atatatat':{'atlas':[1,1,0],'hitbox':[(0,0,1,0.2),(0,0,0.2,1),(0,0.2,1,0.2),(0.8,0,0.2,1)]},
                           'anatatat':{'atlas':[2,1,3],'hitbox':[(0,0,0.2,1),(0,0.8,1,0.2),(0.8,0,0.2,1)]}}},
            'Metal_Floor':{'File':'Assets\\Tiles\\Metal_Floor.png','Rect':[0,0,100,100],
                           'Tile':{'atlas':[0,0],'hitbox':[]},'Layer':0,'overlays':{}},
            'Metal_Wall':{'File':'Assets\\Tiles\\Metal_Wall.png','Rect':[0,0,100,100],
                          'Tile':{'atlas':[0,0],'hitbox':[(0,0,1,1)]},'Layer':50,
                          'overlays':{'ataaaaaa':{'atlas':[1,0,3],'hitbox':[(0,0,1,0.15)]},
                                      'antnaaaa':{'atlas':[2,0,3],'hitbox':[(1,0,0.15)]}}},
            }

    objects = {'Box':{'File':'Assets\\Box.png',
                      'Stats':{'Width':60,'Height':60,'Health':50,'Mass':10}}}

    for obj in objects:
        objects[obj]['Image'] = pygame.image.load(resourcepath(objects[obj]['File'])).convert_alpha()
    
    def process_tile_overlays():
        def rotate_hitbox(hitbox):
            if len(hitbox) == 4:
                tl,tr,bl,br = (hitbox[0],hitbox[1]),(hitbox[0]+hitbox[2],hitbox[1]),(hitbox[0]+hitbox[2],hitbox[1]+hitbox[3]),(hitbox[0],hitbox[1]+hitbox[3])
                rotated = [(1-tl[1],tl[0]),(1-tr[1],tr[0]),(1-bl[1],bl[0]),(1-br[1],br[0])]
                topleft = (min([a[0] for a in rotated]),min([a[1] for a in rotated]))
                bottomright = (max([a[0] for a in rotated]),max([a[1] for a in rotated]))
                new_rec = (topleft[0],topleft[1],bottomright[0]-topleft[0],bottomright[1]-topleft[1])
                return new_rec
            else:
               return (1-hitbox[1],hitbox[0],hitbox[2]) 
        
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

            for o in Data.tile[t]['overlays']:
                Data.tile[t]['overlays'][o]['Layer'] = Data.tile[t]['Layer']
                    
    
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

