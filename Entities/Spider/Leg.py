import pygame,math,random
from Utility_functions import *
from Entities.Spider.Spider_Data import Data

class Leg:
    def __init__(self,player_pos,player_angle,angle,leg_name,body_radius,scale):
        self.scale = scale
        
        stats = Data.Legs[leg_name]['Stats']
        self.leg_lengths = [stats['Length']*scale,stats['Length']*scale]
        self.target_distance = stats['Target_Distance']*scale
        self.leg_start_distance = body_radius*scale*0.7

        self.move_speed = stats['Move_Speed']
        self.move_friction = stats['Move_Friction']
        self.turn_speed = stats['Turn_Speed']
        self.joint_rotate_speed = stats['Joint_Rotate_Speed']
        self.lift_up_distance_max = stats['Lift_Up_Distance_Max']
        self.lift_up_distance_min = stats['Lift_Up_Distance_Min']
        self.prediction_magnitude_velocity = stats['Prediction_Magnitude_Velocity']
        self.prediction_magnitude_angle = stats['Prediction_Magnitude_Angle']
        
        self.base_angle = angle*stats['Forward_Value']

        self.on_ground = True
        self.leg_pos_precision = 0
        self.skeleton = [[length,0] for length in self.leg_lengths]
        self.clockwise = self.base_angle%math.tau<math.pi
        
        self.start_pos = self.get_start_pos(player_pos,player_angle)
        self.ground_target = self.get_ground_target(player_angle)
        self.move(1,player_pos,player_angle,True)

        self.image = Data.Legs[leg_name]['Image']
        self.image = pygame.transform.scale_by(self.image,(self.leg_lengths[0])/(self.image.get_width()-self.image.get_height()))
        self.rotated_images = [pygame.transform.rotate(self.image,angle) for angle in range(360)]
        
    def get_ground_target(self,player_angle,player_velocity=[0,0],player_angular_velocity=0):
        angle = player_angle+self.base_angle+player_angular_velocity*self.prediction_magnitude_angle
        return [self.start_pos[0]+player_velocity[0]*self.prediction_magnitude_velocity+(self.target_distance)*math.cos(angle),
                self.start_pos[1]+player_velocity[1]*self.prediction_magnitude_velocity+(self.target_distance)*math.sin(angle)]

    def move(self,deltatime,player_pos,player_angle,can_lift_up=True,player_velocity=[0,0],player_angular_velocity=0):
        self.start_pos = self.get_start_pos(player_pos,player_angle)
        
        if can_lift_up and distance(self.get_ground_target(player_angle),self.ground_target)>self.target_distance*max(math.e**-self.leg_pos_precision,self.lift_up_distance_min): #distance(self.start_pos,self.ground_target)*1.2>sum(self.leg_lengths) or 
            self.ground_target = self.get_ground_target(player_angle,player_velocity,player_angular_velocity)
            self.on_ground = False
        
        if self.on_ground:
            self.skeleton = self.inverse_kinematics(self.ground_target)
        else:
            self.skeleton = self.inverse_kinematics(self.ground_target,self.joint_rotate_speed*deltatime)

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
            pos = self.start_pos
            for i,skel in enumerate(skeleton):
                prev_angle = prev_angles[i]
                target_angle = skel[1]

                
                if (prev_angle-target_angle)%math.tau<(target_angle-prev_angle)%math.tau:
                    skeleton[i][1] = prev_angle-min(angle_limit,(prev_angle-target_angle)%math.tau)
                else:
                    skeleton[i][1] = prev_angle+min(angle_limit,(target_angle-prev_angle)%math.tau)
                    
##                if tilemap != -1:
##                    circle = (pos[0]+skeleton[i][0]*math.cos(skeleton[i][1]),
##                              pos[1]+skeleton[i][0]*math.sin(skeleton[i][1]),4)
##                    if tilemap.check_collisions(circle):
##                        print(i,'collided',skeleton)
##                        skeleton[i][1] = prev_angle
##                    pos = (pos[0]+skeleton[i][0]*math.cos(skeleton[i][1]),
##                           pos[1]+skeleton[i][0]*math.sin(skeleton[i][1]))
                
                if abs(skeleton[i][1]-target_angle)%math.tau>0.1:
                    complete = False
            if complete:
                self.on_ground = True
                self.leg_pos_precision = -math.log(self.lift_up_distance_max)
                #Data.Sounds['Footstep'].play()
                
        return skeleton
    
    def render(self,Surf,center,player_angle):
        start = self.get_start_pos(center,player_angle)

        pos = start
        for section in self.skeleton:
            pre = pos
            pos = [pos[0]+section[0]*math.cos(section[1]),pos[1]+section[0]*math.sin(section[1])]
##            pygame.draw.line(Surf,(180,120,60),pre,pos,4)
            rotated = self.rotated_images[int(-section[1]/math.pi*180)%360]#pygame.transform.rotate(self.image,-section[1]/math.pi*180)
            Surf.blit(rotated,[pos[0]+(pre[0]-pos[0]-rotated.get_width())/2,pos[1]+(pre[1]-pos[1]-rotated.get_height())/2])
        
