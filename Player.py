import pygame
import sys
from GameState import GameState
from Car import Car
from datetime import datetime
import copy

class Player(GameState):

    START_POS = 70, 370
    FINISH_LINE = [(17, 457), (159, 457)]

    def __init__(self, W, H, win):
        super().__init__(W, H, win)
        self.car = Car(self.START_POS[0], self.START_POS[1])
        self.track = pygame.transform.scale(pygame.image.load("track.png"), (W,H))
        self.lost = False
        self.font = pygame.font.Font(None, 80)
        self.start = datetime.now()
        self.best = self.read_best()
        
    def read_best(self):
        file = open("best.txt", "r")
       
        line = file.readline()
        line = line.split(" ")
    
        return [int(line[1]), int(line[2]), int(line[3])]

    def draw_lost(self):
        lost_text = self.font.render("press R to restart", True, (0,0,0))
        dim = (lost_text.get_width(), lost_text.get_height())
        self.win.blit(lost_text, (self.WIDTH//2-dim[0]//2, self.HEIGHT//2-dim[1]//2))
        pygame.display.update()

    def draw_time(self):
        font = pygame.font.Font(None, 40)
        end = datetime.now()
        delta = end - self.start 
        time_text = font.render(f"{delta.seconds//60}:{delta.seconds%60}.{delta.microseconds//100}", True, (0,0,0))

        if self.best is not None :
            best_text = font.render(f"Best: {self.best[0]}:{self.best[1]}.{self.best[2]}", True, (0,0,0))
            self.win.blit(best_text, (self.WIDTH-best_text.get_width()-10,20))

        self.win.blit(time_text, (20,20))


    def draw(self):
        self.win.blit(self.track, (0,0))

        car_surf = pygame.Surface((self.car.img.get_width(),self.car.img.get_height()))
        car_surf.set_colorkey((0,0,0))
        car_surf.fill((255,0,0))

        rotated_surf = pygame.transform.rotate(car_surf, self.car.angle)
        self.win.blit(rotated_surf, (self.car.x-rotated_surf.get_width()//2, self.car.y-rotated_surf.get_height()//2))
        self.draw_time()
        for point in self.car.get_points():
            pygame.draw.circle(self.win, (0,0,0), (point[0], point[1]), 3)
        pygame.display.update()

    def finished(self):
        delta = datetime.now() - self.start
        if delta.seconds < 1: pass
        elif delta.seconds//60 < self.best[0] or \
            (delta.seconds//60==self.best[0] and delta.seconds%60 < self.best[1]) or \
            (delta.seconds//60==self.best[0] and delta.seconds%60==self.best[1] and delta.microseconds//100<self.best[2]):
            self.best[0] = delta.seconds//60
            self.best[1] = delta.seconds%60
            self.best[2] = delta.microseconds//100

            file = open("best.txt", "r")
            lines = file.readlines()
            lines[0] = f"player {self.best[0]} {self.best[1]} {self.best[2]}"

            file = open("best.txt", "w")
            file.writelines(lines)
            
        self.start = datetime.now()

    def run(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_r:
                    self.car.x = self.START_POS[0]
                    self.car.y = self.START_POS[1]
                    self.car.angle = 270
                    self.lost = False
                    self.start = datetime.now()

        if self.lost: 
            self.draw_lost()
            return self

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:     self.car.rotate(1)
        elif keys[pygame.K_RIGHT]:  self.car.rotate(-1)
        elif keys[pygame.K_DOWN]:   self.car.brake()
        if not keys[pygame.K_DOWN]: self.car.reset_vel()

        self.car.move()
        if self.car.collision(self.track):  self.lost = True

        if self.car.finished(self.FINISH_LINE):
            self.finished()

        self.draw()
        return self