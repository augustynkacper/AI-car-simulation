import pygame
import sys
from GameState import GameState
from Car import Car

class Player(GameState):

    def __init__(self, W, H, win):
        super().__init__(W, H, win)
        self.car = Car(W//2, H//2)
        
        
    
    def draw(self):
        self.win.fill((0,0,0))

        #self.win.blit(self.car.img, (self.car.x, self.car.y))
        pygame.draw.circle(self.win, (255,255,255), (self.car.x, self.car.y), 10)

        pygame.display.update()


    def run(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.car.rotate(-1)
        elif keys[pygame.K_RIGHT]:
            self.car.rotate(1)
        elif keys[pygame.K_DOWN]:
            self.car.brake()
        if not keys[pygame.K_DOWN]:
            self.car.reset_vel()


        self.car.move()
        print(self.car.x, self.car.y)
        self.draw()


        return self