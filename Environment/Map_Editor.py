import os,json
from Environment.Map import *
from Environment.Environment_Data import Data
from Entities.Player import Player
from Entities.Enemy import Enemy
from Camera import Camera
import PyUI as pyui

class Editor_Controller:
    def __init__(self,ui,x,y):
        self.ui = ui
        self.x = x
        self.y = y
        self.keybinds = {'UP':[pygame.K_w,pygame.K_UP],
                         'DOWN':[pygame.K_s,pygame.K_DOWN],
                         'LEFT':[pygame.K_a,pygame.K_LEFT],
                         'RIGHT':[pygame.K_d,pygame.K_RIGHT]}
    def control(self):
        self.speed = 10
        if self.get_pressed('UP'): self.y-=self.speed
        if self.get_pressed('DOWN'): self.y+=self.speed
        if self.get_pressed('LEFT'): self.x-=self.speed
        if self.get_pressed('RIGHT'): self.x+=self.speed
        
    def render_surf(self):
        surf = pygame.Surface((1,1))
        surf.set_alpha(0)
        return surf
    def edit(self,camera,mapp):
        if camera.display_rect.collidepoint(self.ui.mpos):
            pos = camera.screen_pos_to_world_pos(self.ui.mpos,mapp)
            if self.ui.mprs[0]:
                grid_pos = mapp.tilemap.world_pos_to_grid_pos(pos)
                mapp.tilemap.set_tile(grid_pos[0],grid_pos[1],self.ui.IDs['Tile_Picker'].active)

    def get_pressed(self,code):
        if code in self.keybinds:
            for k in self.keybinds[code]:
                if self.ui.kprs[k]:
                    return True
        return False
        
class Map_Editor:
    def __init__(self,ui):
        self.ui = ui
        self.make_gui()
        
        self.map = Map(ui,128)
        self.entities = []
        self.entity_data = []
        self.controller = Editor_Controller(ui,0,0)
        self.camera = Camera(self.controller,pygame.Rect(200,10,990,880),True)

    def game_tick(self,screen):
        screen.fill(pyui.Style.wallpapercol)
        self.camera.move()
        self.camera.render(screen,self.map,[self.controller]+self.entities,[],[],[])
        if self.edit_swapper.active == 'Tilemap':
            self.controller.edit(self.camera,self.map)
        self.controller.control()

    def make_gui(self):
        self.edit_swapper = self.ui.makedropdown(10,15,['Tilemap','Entities','Objects'],width=180,dropsdown=False,command=self.swap_menu)

        self.ui.makebutton(15,820,'Save',width=160,command=lambda: self.ui.movemenu('save_map','down')),
        self.ui.makebutton(15,860,'Open',width=160,command=self.open_menu_init),
            
        #### Tile Map
        self.tilemap_editor = self.ui.makewindow(10,50,180,600,autoshutwindows=['tilemap_editor','entity_editor','object_editor'],ID='tilemap_editor',bounditems=[
            self.ui.makedropdown(10,20,[a for a in Data.tile.keys()],width=160,ID='Tile_Picker',layer=5),
            ])
        self.ui.makewindowedmenu(10,10,180,160,'save_map')
        self.ui.maketext(90,4,'{"Save" underlined=True}',menu='save_map',objanchor=('w/2',0)),
        self.ui.maketextbox(90,40,'',width=160,lines=3,objanchor=('w/2',0),menu='save_map',ID='save_textbox',command=self.save_file),
        self.ui.makebutton(90,120,'Save',objanchor=('w/2',0),menu='save_map',command=self.save_file),

        self.ui.makewindowedmenu(10,10,180,160,'open_map',ID='open_map_menu')
        self.ui.maketext(90,4,'{"Open" underlined=True}',menu='open_map',objanchor=('w/2',0)),
        self.ui.maketable(90,35,titles=['File Names'],menu='open_map',objanchor=('w/2',0),ID='files_open_table'),
        
        ### Entities
        self.entity_editor = self.ui.makewindow(10,50,180,600,autoshutwindows=['tilemap_editor','entity_editor','object_editor'],ID='entity_editor',bounditems=[
            self.ui.makebutton(10,10,'Add Spider',width=160,command=self.add_spider),
            self.ui.maketable(10,50,titles=['Spiders'],width=160,ID='spider_table'),

            ])
        self.ui.makewindowedmenu(10,10,180,340,'edit_spider')
        self.ui.maketextbox(10,25,'0',160,ID='edit_spider_x',command=self.pull_spider_info,attachscroller=False,intscroller=True,numsonly=True,menu='edit_spider',bounditems=[
            self.ui.maketext(0,-23,'X pos')])
        self.ui.maketextbox(10,80,'0',160,ID='edit_spider_y',command=self.pull_spider_info,attachscroller=False,intscroller=True,numsonly=True,menu='edit_spider',bounditems=[
            self.ui.maketext(0,-23,'Y pos')])
        self.ui.maketextbox(10,135,'0',160,ID='edit_spider_leg',command=self.pull_spider_info,attachscroller=False,menu='edit_spider',bounditems=[
            self.ui.maketext(0,-23,'Leg Name')])
        self.ui.maketextbox(10,190,'0',160,ID='edit_spider_body',command=self.pull_spider_info,attachscroller=False,menu='edit_spider',bounditems=[
            self.ui.maketext(0,-23,'Body Name')])
        self.ui.maketextbox(10,245,'0',160,ID='edit_spider_weapon',command=self.pull_spider_info,attachscroller=False,menu='edit_spider',bounditems=[
            self.ui.maketext(0,-23,'Weapon Name')])
        self.ui.makebutton(10,280,'Delete',command=self.delete_spider,menu='edit_spider')
        
        
    
        ### Objects
        self.object_editor = self.ui.makewindow(10,50,180,600,autoshutwindows=['tilemap_editor','entity_editor','object_editor'],ID='object_editor',bounditems=[
            
            ])

        self.swap_menu()
        
    def open_menu_init(self):
        table = self.ui.IDs['files_open_table']
        files = os.listdir(resourcepath('Maps'))
        data = []
        for f in files:
            if '.json' in f:
                func = pyui.funcer(self.open_file,name=resourcepath('Maps\\'+f))
                data.append([self.ui.makebutton(0,0,f.removesuffix('.json'),command=func.func)])
        table.data = data
        table.refresh()
        self.ui.IDs['open_map_menu'].setheight(table.height+35+10)
        
        
        self.ui.movemenu('open_map','down')
        
    def save_file(self):
        dat = {'map':self.map.get_storable_map(),
               'entities':self.entity_data}
        
        with open(resourcepath('Maps\\'+self.ui.IDs['save_textbox'].text+'.json'),'w') as f:
            json.dump(dat,f)
            
        self.ui.IDs['save_textbox'].settext()
        self.ui.menuback()
    def open_file(self,name):
        if name == '':
            dat = {'map':{'tilemap':[['Metal_Floor']],'pos':[0,0]},
                   'entities':{}}
        else:
            if not '.json' in name:
                name  = resourcepath('Maps\\'+name+'.json')
            with open(name,'r') as f:
                dat = json.load(f)
        self.map.load_map(dat['map']['tilemap'],dat['map']['pos'])
        self.entity_data = dat['entities']
        self.refresh_entities()
        self.ui.menuback()

    def swap_menu(self):
        if self.edit_swapper.active == 'Tilemap':
            self.tilemap_editor.open()
        elif self.edit_swapper.active == 'Entities':
            self.entity_editor.open()
        elif self.edit_swapper.active == 'Objects':
            self.object_editor.open()

    def refresh_entities(self):
        data = []
        self.entities = []
        for i,info in enumerate(self.entity_data):
            func = pyui.funcer(self.edit_spider,index=i)
            data.append([self.ui.makebutton(0,0,info['ID'],command=func.func)])
            self.entities.append(Map_Editor.make_spider(self.ui,info))
        self.ui.IDs['spider_table'].data = data
        self.ui.IDs['spider_table'].refresh()
        

    def add_spider(self):
        dat = {'ID':'Player','x_pos':0,'y_pos':0,'Leg':'Base','Body':'Base','Weapon':'Base'}
        if len(self.entity_data)>0:
            dat['ID'] = 'Spider'+str(len(self.entity_data))
        self.entity_data.append(dat)

        self.refresh_entities()

    def make_spider(ui,info):
        try:
            if info['ID'] == 'Player':
                return Player(ui,info['x_pos'],info['y_pos'],
                              info['Leg'],info['Body'],info['Weapon'])
            else:
                return Enemy(ui,info['x_pos'],info['y_pos'],
                              info['Leg'],info['Body'],info['Weapon'])
        except:
            print('Failed to make '+info['ID'])
            return Enemy(ui,0,0,'Base','Base','Base')
    def delete_spider(self):
        del self.entity_data[self.spider_edit_index]
        self.refresh_entities()
        self.ui.menuback()
    def edit_spider(self,index):
        self.spider_edit_index = index
        info = self.entity_data[index]
        self.ui.IDs['edit_spider_x'].settext(str(info['x_pos']))
        self.ui.IDs['edit_spider_y'].settext(str(info['y_pos']))
        self.ui.IDs['edit_spider_leg'].settext(str(info['Leg']))
        self.ui.IDs['edit_spider_body'].settext(str(info['Body']))
        self.ui.IDs['edit_spider_weapon'].settext(str(info['Weapon']))
        self.ui.movemenu('edit_spider','down')
    def pull_spider_info(self):
        index = self.spider_edit_index
        self.entity_data[index]['x_pos'] = int(self.ui.IDs['edit_spider_x'].text)
        self.entity_data[index]['y_pos'] = int(self.ui.IDs['edit_spider_y'].text)
        self.entity_data[index]['Leg'] = self.ui.IDs['edit_spider_leg'].text
        self.entity_data[index]['Body'] = self.ui.IDs['edit_spider_body'].text
        self.entity_data[index]['Weapon'] = self.ui.IDs['edit_spider_weapon'].text
        self.refresh_entities()



        
        

    
