from Player import Player

from Map import Map
import PyUI as pyui

class Level:
    def __init__(self,ui):
        self.ui = ui
        
        self.players = [Player(0,0,True)]
    def game_tick(self,screen):
        screen.fill(pyui.Style.wallpapercol)
