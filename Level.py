from Player import Player
from Camera import Camera
import pygame

from Map import Map
import PyUI as pyui

class Level:
    def __init__(self,ui):
        self.ui = ui

        self.players = [Player(ui,0,0)]
        self.cameras = [Camera(self.players[0],pygame.Rect(10,10,ui.screenw-20,ui.screenh-20))]
        self.map = Map(128)
        
    def game_tick(self,screen):
        screen.fill(pyui.Style.wallpapercol)

        for c in self.cameras:
            c.move()
            c.render(screen,self.map,self.players)

        for p in self.players:
            p.control()
