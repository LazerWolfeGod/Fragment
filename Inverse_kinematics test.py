import pygame,math,random,sys,os
import PyUI as pyui
from Utility_functions import *

pygame.init()
screenw = 600
screenh = 600
screen = pygame.display.set_mode((screenw, screenh),pygame.RESIZABLE)
ui = pyui.UI()
done = False
clock = pygame.time.Clock()

# length, angle
arm = [[80,0],[140,0]]
center = (300,300)
target = (500,300)

def solve(center,arm,target):
    d = distance(center,target)
    L1 = arm[0][0]
    L2 = arm[1][0]

    arm[0][1] = math.atan2(target[1]-center[1],target[0]-center[0])

##    if target[0]<center[0]:
##        invert = 1
##        arm[0][1]*=-1
##    else: invert = -1
    invert = -1

    arm[0][1]*=-invert
    
    if L1+L2<d:
        arm[1][1] = arm[0][1]
    elif d <= abs(L2-L1): arm[1][1] = arm[0][1]+math.pi
    else:
        arm[0][1] += math.acos((d**2+L1**2-L2**2)/(2*d*L1))*invert
        arm[1][1] = arm[0][1]+(math.pi-math.acos((L2**2+L1**2-d**2)/(2*L2*L1)))*-invert
    return arm

def draw(center,arm,target):
    pos = center
    for a in arm:
        pre = pos
        pos = [pos[0]+a[0]*math.cos(a[1]),pos[1]+a[0]*math.sin(a[1])]
        pygame.draw.line(screen,(255,0,(a[1]%math.pi)*255/3.2),pre,pos,4)
    pygame.draw.circle(screen,(0,0,255),target,10)

while not done:
    for event in ui.loadtickdata():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(pyui.Style.wallpapercol)
    target = ui.mpos
    arm = solve(center,arm,target)
    
    draw(center,arm,target)
    ui.rendergui(screen)
    pygame.display.flip()
    clock.tick(60)                                               
pygame.quit() 
