from Player import Player
from Camera import Camera
import pygame

from Environment.Map import Map
import PyUI as pyui

class Level:
    def __init__(self,ui):
        self.ui = ui

        self.players = [Player(ui,240,240)]
        self.cameras = [Camera(self.players[0],pygame.Rect(10,10,ui.screenw-20,ui.screenh-20))]
        self.map = Map(128,'Level 1')

        self.projectiles = []
        self.particles = []
        
    def game_tick(self,screen):
        screen.fill(pyui.Style.wallpapercol)

        for c in self.cameras:
            c.move()
            c.render(screen,self.map,self.players,self.projectiles,self.particles)

        for p in self.players:
            p.control(self.map.tilemap,self.projectiles)
            p.move_spider(self.map.tilemap,self.ui.deltatime)

        for object_list in [self.projectiles,self.particles]:
            remove_list = []
            for p in object_list:
                p.move(self.map.tilemap,self.particles)
                if p.check_finished():
                    remove_list.append(p)
            for rem in remove_list:
                object_list.remove(rem)
