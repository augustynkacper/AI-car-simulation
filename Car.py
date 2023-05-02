import math
import pygame

ROTATE_VEL = 3
VELOCITY = 5
BRAKE_DECR = 1
LOWEST_BRAKE_VEL = 2

class Car:
    vel = VELOCITY
    angle = 270

    def __init__(self, x, y, win):
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

    def collision(self, track):
        front_center_x = self.x + math.cos(self.angle*math.pi/180) * self.length//2
        front_center_y = self.y - math.sin(self.angle*math.pi/180) * self.length//2

        track_color = track.get_at((int(front_center_x), int(front_center_y)))
        color = (55, 125, 33, 255)
        delta = 10
        flag = True

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