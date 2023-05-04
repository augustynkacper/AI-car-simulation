import math
import pygame
from datetime import datetime

ROTATE_VEL = 6
VELOCITY = 5
BRAKE_DECR = 1
LOWEST_BRAKE_VEL = 2

class Car:
    vel = VELOCITY
    angle = 270

    def __init__(self, x, y, angle=270):
        self.x = x
        self.y = y
        self.width = 50
        self.length = 80
        self.angle = angle
        self.img = pygame.transform.rotate(
            pygame.transform.scale(
                pygame.image.load("car.png").convert_alpha(), (self.width,self.length)
            ), -90 ) 

        self.distance = 0   
        self.start = datetime.now()    

    def rotate(self, a):
        self.angle += ROTATE_VEL * a
        #self.img = pygame.transform.rotate(self.img, ROTATE_VEL * a)
        if (self.angle > 360): 
            self.angle -= 360
        elif (self.angle < 0): 
            self.angle += 360

    def brake(self):
        self.vel -= 1
        self.vel = max(LOWEST_BRAKE_VEL, self.vel)

    def reset_vel(self):
        self.vel += 0.2
        self.vel = min(VELOCITY, self.vel)

    def move(self):
        self.y -= math.sin(self.angle*math.pi/180) * self.vel
        self.x += math.cos(self.angle*math.pi/180) * self.vel

        self.distance += self.vel

    

    # returns car collision points in order:
    # left_side, left_top, front, right_top, right_side
    def get_points(self):

        angle = self.angle+90
        left_side_x = self.x + math.cos(angle*math.pi/180) * self.width//2
        left_side_y = self.y - math.sin(angle*math.pi/180) * self.width//2

        angle = self.angle + math.degrees(math.atan(self.width/self.length))
        l = ((self.length/2)**2+(self.width/2)**2)**0.5
        left_top_x = self.x + math.cos(angle*math.pi/180) * l
        left_top_y = self.y - math.sin(angle*math.pi/180) * l

        angle = self.angle
        front_center_x = self.x + math.cos(angle*math.pi/180) * self.length//2
        front_center_y = self.y - math.sin(angle*math.pi/180) * self.length//2

        angle = self.angle-math.degrees(math.atan(self.width/self.length))
        right_top_x = self.x + math.cos(angle*math.pi/180) * l
        right_top_y = self.y - math.sin(angle*math.pi/180) * l

        angle = self.angle-90
        right_side_x = self.x + math.cos(angle*math.pi/180) * self.width//2
        right_side_y = self.y - math.sin(angle*math.pi/180) * self.width//2

        res = []
        res.append((left_side_x, left_side_y))
        res.append((left_top_x, left_top_y))
        res.append((front_center_x, front_center_y))
        res.append((right_top_x, right_top_y)) 
        res.append((right_side_x, right_side_y))
        return res



    def get_distances(self, track):
        collision_points = self.get_points()
        
        res = []
        color = (55, 125, 33, 255)
        delta = 20

        a = math.degrees(math.atan(self.width/self.length))
        for i, alpha in enumerate([90, a, 0, -a, -90]):
            x, y = collision_points[i]
            angle = self.angle + alpha
            l = 0
            while 0<=x<track.get_width() and 0<=y<track.get_height() and not self.cmp(color, track.get_at((int(x), int(y))), delta):
                l += 1
                x = self.x + math.cos(angle*math.pi/180) * l
                y = self.y - math.sin(angle*math.pi/180) * l
            res.append((x,y))
        
        #dist = [math.dist(res[i], collision_points[i]) for i in range(len(res))]
        dist = [math.dist(res[i], (self.x,self.y)) for i in range(len(res))]
        #dist[0] = dist[0] * 10
        #dist[4] = dist[4] * 10
        return dist 

    def get_reward(self):
        delta = self.start - datetime.now()

        tm = delta.seconds + delta.microseconds
        
        return self.distance/50.0

        

    # True if colors are the same
    def cmp(self,color1, color2, delta):
        flag = True 
        for i in range(3):
            if abs(color1[i]-color2[i]) > delta:
                return False
        return True

    # for every collision point, check if outside of track
    def collision(self, track):
        points = self.get_points()
        
        color = (55, 125, 33, 255)
        delta = 10
        
        for point in points:
            x,y = int(point[0]), int(point[1])
            if not (0<=x<track.get_width() and 0<=y<track.get_height()): 
                return True
            track_color = track.get_at((x,y))
            if self.cmp(track_color,color,  delta):
                return True 
        return False

    def finished(self, line):
        delta = VELOCITY//2

        if line[0][0] <= self.x <= line[1][0]:
            if line[0][1]-delta <= self.y <= line[0][1]+delta:
                return True 

        return False