import math
import pygame

ROTATE_VEL = 3
VELOCITY = 5
BRAKE_DECR = 1
LOWEST_BRAKE_VEL = 2

class Car:
    vel = VELOCITY
    angle = 270

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.length = 80
        self.img = pygame.transform.rotate(
            pygame.transform.scale(
                pygame.image.load("car.png").convert_alpha(), (self.width,self.length)
            ), -90 )        

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
        self.y += -math.sin(self.angle*math.pi/180) * self.vel
        self.x += math.cos(self.angle*math.pi/180) * self.vel

    def get_points(self):
        front_center_x = self.x + math.cos(self.angle*math.pi/180) * self.length//2
        front_center_y = self.y - math.sin(self.angle*math.pi/180) * self.length//2

        angle_right_side = self.angle-90 if self.angle > 90 else 270+self.angle 
        right_side_x = self.x + + math.cos(angle_right_side*math.pi/180) * self.width//2
        right_side_y = self.y - math.sin(angle_right_side*math.pi/180) * self.width//2

        left_side_x = self.x + (self.x-right_side_x)
        left_side_y = self.y + (self.y-right_side_y)

        _x = (front_center_x+right_side_x)/2
        _y = (front_center_y+right_side_y)/2

        right_top_x = _x + (_x-self.x)
        right_top_y = _y + (_y-self.y)

        left_top_x = front_center_x + (front_center_x-right_top_x)
        left_top_y = front_center_y + (front_center_y-right_top_y)

        res = []
        res.append((front_center_x, front_center_y))
        res.append((right_top_x, right_top_y))
        res.append((left_top_x, left_top_y))
        res.append((right_side_x, right_side_y))
        res.append((left_side_x, left_side_y))

        return res


    def collision(self, track):
        points = self.get_points()
        
        color = (55, 125, 33, 255)
        delta = 10
        flag = True

        for point in points:
            track_color = track.get_at((int(point[0]), int(point[1])))
            for i in range(3) :
                if not(color[i]+delta >= track_color[i] >=color[i]-delta):
                    flag = False
        return flag

    def finished(self, line):
        delta = VELOCITY//2

        if line[0][0] <= self.x <= line[1][0]:
            if line[0][1]-delta <= self.y <= line[0][1]+delta:
                return True 

        return False