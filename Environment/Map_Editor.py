import os
from Environment.Map import *
from Environment.Environment_Data import Data
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
        
        self.map = Map(100)
        self.controller = Editor_Controller(ui,0,0)
        self.camera = Camera(self.controller,pygame.Rect(200,10,990,880),True)

    def game_tick(self,screen):
        screen.fill(pyui.Style.wallpapercol)
        self.camera.move()
        self.camera.render(screen,self.map,[self.controller],[],[])
        self.controller.edit(self.camera,self.map)
        self.controller.control()

    def make_gui(self):
        self.ui.makedropdown(10,20,[a for a in Data.tile.keys()],width=180,ID='Tile_Picker',layer=5)

        ## save
        self.ui.makebutton(15,70,'Save',width=180,command=lambda: self.ui.movemenu('save_map','down'))
        self.ui.makewindowedmenu(10,10,180,160,'save_map')
        self.ui.maketext(90,4,'{"Save" underlined=True}',menu='save_map',objanchor=('w/2',0))
        self.ui.maketextbox(90,40,'',width=160,lines=3,objanchor=('w/2',0),menu='save_map',ID='save_textbox',command=self.save_file)
        self.ui.makebutton(90,120,'Save',objanchor=('w/2',0),menu='save_map',command=self.save_file)

        ## open
        self.ui.makebutton(15,110,'Open',width=180,command=self.open_menu_init)
        self.ui.makewindowedmenu(10,10,180,160,'open_map')
        self.ui.maketext(90,4,'{"Open" underlined=True}',menu='open_map',objanchor=('w/2',0))
        self.ui.maketable(90,40,titles=['File Names'],menu='open_map',objanchor=('w/2',0),ID='files_open_table')


    def open_menu_init(self):
        table = self.ui.IDs['files_open_table']
        files = os.listdir(resourcepath('Maps'))
        print(files)
        data = []
        for f in files:
            func = pyui.funcer(self.open_file,file=resourcepath('Maps\\'+f))
            data.append([self.ui.makebutton(0,0,f.removesuffix('.json'),command=func.func)])
        table.data = data
        table.refresh()
        
        
        self.ui.movemenu('open_map','down')
        
    def save_file(self):
        self.map.save_map(self.ui.IDs['save_textbox'].text)
        self.ui.IDs['save_textbox'].settext()
        self.ui.menuback()
    def open_file(self,file):
        self.map.load_map(file)
        self.ui.menuback()

    
