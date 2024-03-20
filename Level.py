from Player import Player
from Enemy import Enemy
from Camera import Camera
import pygame

from Environment.Map import Map
import PyUI as pyui

class Level:
    def __init__(self,ui):
        self.ui = ui

        self.entities = [Player(ui,240,240),Enemy(ui,360,360)]
        self.cameras = [Camera(self.entities[0],pygame.Rect(10,10,ui.screenw-20,ui.screenh-20))]
        self.map = Map(128,'massive')

        self.projectiles = []
        self.particles = []
        
    def game_tick(self,screen):
        screen.fill(pyui.Style.wallpapercol)

        for c in self.cameras:
            c.move()
            c.render(screen,self.map,self.entities,self.projectiles,self.particles)

        remove_list = []
        for p in self.entities:
            p.control(self.map.tilemap,self.projectiles,self.entities)
            p.move_spider(self.map.tilemap,self.ui.deltatime)
            if p.check_dead(self.particles):
                remove_list.append(p)
        for rem in remove_list:
            self.entities.remove(rem)

        for object_list in [self.projectiles,self.particles]:
            remove_list = []
            for p in object_list:
                p.move(self.map.tilemap,self.particles)
                if p.check_finished():
                    remove_list.append(p)
            for rem in remove_list:
                object_list.remove(rem)
        for p in self.projectiles:
            p.check_entity_collide(self.entities)
