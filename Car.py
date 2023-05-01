import math
import pygame

ROTATE_VEL = 4
VELOCITY = 5
BRAKE_DECR = 1
LOWEST_BRAKE_VEL = 2

class Car:
    vel = VELOCITY
    angle = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.transform.rotate(
            pygame.transform.scale(
                pygame.image.load("car.png"), (50,80)
            ), -45 )

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
        x_coeff, y_coeff = 1, 1
        ang = 0
        
        if 0<=self.angle<=90:
            x_coeff, y_coeff = 1, 1
            ang = self.angle 
        elif 90<self.angle<=180:
            x_coeff, y_coeff = -1, 1
            ang = 180-self.angle     
        elif 180<self.angle<=270:
            x_coeff, y_coeff = -1, -1
            ang = self.angle - 180 
        elif 270<self.angle<=360:
            x_coeff, y_coeff = 1, -1
            ang = 360 - self.angle 
            
        dy = y_coeff * math.sin(ang*math.pi/180) * self.vel
        self.y += dy
        self.x += x_coeff * math.sqrt(self.vel**2 - dy**2)
        #self.y = int(self.y)
        #self.x = int(self.x)

