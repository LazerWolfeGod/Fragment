from Entities.Player import Player
from Entities.Enemy import Enemy
from Entities.Objects import *
from Camera import Camera
import pygame,random

from Environment.Map import Map
import PyUI as pyui

class Level:
    def __init__(self,ui):
        self.ui = ui

        self.entities = [Player(ui,240,240),Enemy(ui,360,360)]
        self.objects = [Box(ui,random.gauss(300,50),random.gauss(200,50)) for i in range(50)]
        self.cameras = [Camera(self.entities[0],pygame.Rect(10,10,ui.screenw-20,ui.screenh-20))]
        self.map = Map(ui,128,'massive')

        self.projectiles = []
        self.particles = []
        
    def game_tick(self,screen):
        screen.fill(pyui.Style.wallpapercol)

        for c in self.cameras:
            c.move()
            c.render(screen,self.map,self.entities,self.objects,self.projectiles,self.particles)

        remove_list = []
        for p in self.entities+self.objects:
            p.gametick(self.map,self.projectiles,self.entities,self.ui.deltatime)
##            p.control(self.map,self.projectiles,self.entities)
##            p.move(self.map,self.ui.deltatime)
            if p.check_dead(self.particles):
                remove_list.append(p)
        for rem in remove_list:
            if rem in self.entities: self.entities.remove(rem)
            else: self.objects.remove(rem)

        for object_list in [self.projectiles,self.particles]:
            remove_list = []
            for p in object_list:
                p.move(self.map,self.entities,self.objects,self.particles)
                if p.check_finished():
                    remove_list.append(p)
            for rem in remove_list:
                rem.finish(self.particles)
                object_list.remove(rem)
##        for p in self.projectiles:
##            p.check_entity_collide(self.entities+self.objects)
