import pygame,math,random
import PyUI as pyui
from Projectile import *
from Utility_functions import *

class Leg:
    def __init__(self,player_pos,player_angle,angle,target_distance,leg_start_distance,leg_lengths):
        self.target_distance = target_distance
        self.base_angle = angle
        self.leg_start_distance = leg_start_distance
        self.leg_lengths = leg_lengths
        self.on_ground = True
        self.leg_pos_precision = 0
        self.skeleton = [[length,0] for length in self.leg_lengths]
        self.clockwise = self.base_angle%math.tau<math.pi
        
        self.start_pos = self.get_start_pos(player_pos,player_angle)
        self.ground_target = self.get_ground_target(player_angle)
        self.move(player_pos,player_angle,True)

        self.img = pygame.image.load(resourcepath('Assets\\Player_parts\\Leg.png'))
        self.img = pygame.transform.scale_by(self.img,(self.leg_lengths[0])/(self.img.get_width()-self.img.get_height()))
        

    def get_ground_target(self,player_angle,player_velocity=[0,0],player_angular_velocity=0):
        self.predicition_magnitude = 10
        angle = player_angle+self.base_angle+player_angular_velocity*self.predicition_magnitude
        return [self.start_pos[0]+player_velocity[0]*self.predicition_magnitude+(self.target_distance)*math.cos(angle),
                self.start_pos[1]+player_velocity[1]*self.predicition_magnitude+(self.target_distance)*math.sin(angle)]

    def move(self,player_pos,player_angle,can_lift_up,player_velocity=[0,0],player_angular_velocity=0):
        self.start_pos = self.get_start_pos(player_pos,player_angle)
        
        if can_lift_up and distance(self.get_ground_target(player_angle),self.ground_target)>self.target_distance*max(math.e**-self.leg_pos_precision,0.3): #distance(self.start_pos,self.ground_target)*1.2>sum(self.leg_lengths) or 
            self.ground_target = self.get_ground_target(player_angle,player_velocity,player_angular_velocity)
            self.on_ground = False
        
        if self.on_ground:
            self.skeleton = self.inverse_kinematics(self.ground_target)
        else:
            self.skeleton = self.inverse_kinematics(self.ground_target,0.3)

        self.leg_pos_precision += 0.1
        
            
    def get_start_pos(self,player_pos,player_angle):
        return [player_pos[0]+(self.leg_start_distance)*math.cos(player_angle+self.base_angle),
                player_pos[1]+(self.leg_start_distance)*math.sin(player_angle+self.base_angle)]
        
    def inverse_kinematics(self,target,angle_limit=10):
        d = distance(self.start_pos,target)
        if angle_limit!=10:
            prev_angles = [a[1] for a in self.skeleton]
            
        L1 = self.leg_lengths[0]
        L2 = self.leg_lengths[1]

        skeleton = [[L1,0],[L2,0]]

        skeleton[0][1] = math.atan2(target[1]-self.start_pos[1],target[0]-self.start_pos[0])


        if self.clockwise:
            invert = 1
            skeleton[0][1]*=-1
        else: invert = -1

        skeleton[0][1]*=-invert
        
        if L1+L2<d:
            skeleton[1][1] = skeleton[0][1]
        elif d <= abs(L2-L1): skeleton[1][1] = skeleton[0][1]+math.pi
        else:
            skeleton[0][1] += math.acos((d**2+L1**2-L2**2)/(2*d*L1))*invert
            skeleton[1][1] = skeleton[0][1]+(math.pi-math.acos((L2**2+L1**2-d**2)/(2*L2*L1)))*-invert

        if angle_limit!=10:
            complete = True
            for i,skel in enumerate(skeleton):
                prev_angle = prev_angles[i]
                target_angle = skel[1]
                
                if (prev_angle-target_angle)%math.tau<(target_angle-prev_angle)%math.tau:
                    skeleton[i][1] = prev_angle-min(angle_limit,(prev_angle-target_angle)%math.tau)
                else:
                    skeleton[i][1] = prev_angle+min(angle_limit,(target_angle-prev_angle)%math.tau)
                if abs(skeleton[i][1]-target_angle)%math.tau>0.1:
                    complete = False
            if complete:
                self.on_ground = True
                self.leg_pos_precision = 0
                
        return skeleton
    
    def render(self,Surf,center,player_angle):
        start = self.get_start_pos(center,player_angle)

        pos = start
        for section in self.skeleton:
            pre = pos
            pos = [pos[0]+section[0]*math.cos(section[1]),pos[1]+section[0]*math.sin(section[1])]
##            pygame.draw.line(Surf,(180,120,60),pre,pos,4)
            rotated = pygame.transform.rotate(self.img,-section[1]/math.pi*180)
            Surf.blit(rotated,[pos[0]+(pre[0]-pos[0]-rotated.get_width())/2,pos[1]+(pre[1]-pos[1]-rotated.get_height())/2])
        

class Player:
    def __init__(self,ui,x,y):
        self.ui = ui
        self.x = x
        self.y = y
        self.velocity = pygame.Vector2()
        self.angular_velocity = 0
        self.angle = 0
        self.target_angle = 0
        
        self.move_acceleration = 0.5
        self.move_friction = 0.85
        self.turn_acceleration = 0.2
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
        self.num_legs = 6
        self.legs = [Leg([self.x,self.y],self.angle,theta/self.num_legs*math.tau+math.pi/self.num_legs,self.radius*2,self.radius*0.7,[self.radius*1.4,self.radius*1.4]) for theta in range(self.num_legs)]

    def render_surf(self):
        center = (self.radius*3,self.radius*3)
        Surf = pygame.Surface((self.radius*6,self.radius*6),pygame.SRCALPHA)
 
        pygame.draw.circle(Surf,(150,100,60),center,self.radius)

        for leg in self.legs:
            leg.render(Surf,center,self.angle)
        return Surf

    def control(self,tilemap,projectiles):
        delta_vel = pygame.Vector2()
        if self.get_pressed('UP'): delta_vel[1]-=1 
        if self.get_pressed('DOWN'): delta_vel[1]+=1
        if self.get_pressed('LEFT'): delta_vel[0]-=1
        if self.get_pressed('RIGHT'): delta_vel[0]+=1
        if delta_vel.magnitude()>0: delta_vel.normalize_ip()
        delta_vel*=self.move_acceleration*self.ui.deltatime
        
        self.velocity+=delta_vel
        

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

        for leg in self.legs:
            leg.move([self.x,self.y],self.angle,sum([l.on_ground for l in self.legs])>int(len(self.legs)/2),self.velocity,self.angular_velocity)

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

    
        
