import pygame,math,random
import PyUI as pyui
from Projectile import *
from Utility_functions import *


def inverse_kinematics(center,leg_lengths,target):
    d = distance(center,target)
    L1 = leg_lengths[0]
    L2 = leg_lengths[1]

    skeleton = [[0,0],[0,0]]

    skeleton[0][1] = math.atan2(target[1]-center[1],target[0]-center[0])
    if target[0]<center[0]: skeleton[0][1]*=-1

    if target[0]<center[0]: invert = 1
    else: invert = -1

    skeleton[0][1]*=-invert
    
    if L1+L2<d:
        skeleton[1][1] = skeleton[0][1]
    elif d <= abs(L2-L1): skeleton[1][1] = skeleton[0][1]+math.pi
    else:
        skeleton[0][1] += math.acos((d**2+L1**2-L2**2)/(2*d*L1))*invert
        skeleton[1][1] = skeleton[0][1]+(math.pi-math.acos((L2**2+L1**2-d**2)/(2*L2*L1)))*-invert
    return skeleton

class Player:
    def __init__(self,ui,x,y):
        self.ui = ui
        self.x = x
        self.y = y
        self.velocity = [0,0]
        self.angular_velocity = 0
        self.angle = 0
        self.target_angle = 0
        
        self.move_acceleration = 1
        self.move_friction = 0.85
        self.turn_acceleration = 0.5
        self.restitution_coefficient = 0.2

        self.radius = 15
        
        self.keybinds = {'UP':[pygame.K_w,pygame.K_UP],
                         'DOWN':[pygame.K_s,pygame.K_DOWN],
                         'LEFT':[pygame.K_a,pygame.K_LEFT],
                         'RIGHT':[pygame.K_d,pygame.K_RIGHT],
                         'SHOOT':[pygame.K_SPACE],
                         'DASH':[pygame.K_SPACE]}

        self.mpos = (0,0)
        self.make_legs()

    def make_legs(self):
        self.legs = 4
        self.leg_physics()

    def leg_physics(self):
        skeleton_lengths = [self.radius*1.5,self.radius*1.5]
        length = self.radius*2.5
        self.leg_targets = [(length*math.cos(theta/self.legs*math.tau+math.pi/4+self.angle),
                             length*math.sin(theta/self.legs*math.tau+math.pi/4+self.angle)) for theta in range(self.legs)]

        self.leg_sections = [inverse_kinematics((self.x,self.y),skeleton_lengths,target) for target in self.leg_targets]
        
    def render_surf(self):
        center = (self.radius*2,self.radius*2)
        Surf = pygame.Surface((self.radius*4,self.radius*4),pygame.SRCALPHA)

        for leg_pos in self.leg_targets:
            pygame.draw.line(Surf,(130,90,60),center,(center[0]+leg_pos[0],center[1]+leg_pos[1]),int(self.radius/4))

        pygame.draw.circle(Surf,(150,100,60),center,self.radius)

        for leg in self.leg_sections:
            pos = center
            for section in leg:
                pre = pos
                pos = [pos[0]+section[0]*math.cos(section[1]),pos[1]+section[0]*math.sin(section[1])]
                pygame.draw.line(screen,(180,120,60),pre,pos,4)

            
        return Surf

    def control(self,tilemap,projectiles):
        if self.get_pressed('UP'): self.velocity[1]-=self.move_acceleration*self.ui.deltatime
        if self.get_pressed('DOWN'): self.velocity[1]+=self.move_acceleration*self.ui.deltatime
        if self.get_pressed('LEFT'): self.velocity[0]-=self.move_acceleration*self.ui.deltatime
        if self.get_pressed('RIGHT'): self.velocity[0]+=self.move_acceleration*self.ui.deltatime

        self.target_angle = math.atan2(self.mpos[1]-self.y,self.mpos[0]-self.x)
        if (self.angle-self.target_angle)%math.tau<(self.target_angle-self.angle)%math.tau:
            self.angular_velocity-=min(self.turn_acceleration,(self.angle-self.target_angle)%math.tau)
        else:
            self.angular_velocity+=min(self.turn_acceleration,(self.target_angle-self.angle)%math.tau)

        self.angular_velocity*=0.3
        self.angle+=self.angular_velocity

        self.velocity[0]*=self.move_friction**self.ui.deltatime
        self.velocity[1]*=self.move_friction**self.ui.deltatime

        prev_x = self.x
        self.x+=self.velocity[0]*self.ui.deltatime
        if self.get_tilemap_collision(tilemap):
            self.x = prev_x
            self.velocity[0]*=-self.restitution_coefficient

        prev_y = self.y
        self.y+=self.velocity[1]*self.ui.deltatime
        if self.get_tilemap_collision(tilemap):
            self.y = prev_y
            self.velocity[1]*=-self.restitution_coefficient
        

        if self.get_pressed('SHOOT'):
            self.shoot(projectiles)

        self.leg_physics()

    def get_pressed(self,code):
        if code in self.keybinds:
            for k in self.keybinds[code]:
                if self.ui.kprs[k]:
                    return True
        return False

    def shoot(self,projectiles):
        projectiles.append(Fader(self.ui,self.x,self.y,self.angle+random.gauss(0,0.1)))

    def get_tilemap_collision(self,tilemap):
        return tilemap.check_collisions((self.x,self.y,self.radius))

    
        
