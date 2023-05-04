import pygame
import sys
from GameState import GameState
import neat
from Car import Car

class AICar(GameState):

    START_POS = 70, 370
    FINISH_LINE = [(17, 457), (159, 457)]

    def __init__(self, W, H, win):
        super().__init__(W, H, win)
        type="ai"
        self.cars = []
        self.track = pygame.transform.scale(pygame.image.load("track3.png"), (W,H))
        self.best = self.read_best()
        self.generation = 0

    def read_best(self):
        file = open("best.txt", "r")
        line = file.readline()
        line = line.split(" ")
        return [int(line[1]), int(line[2]), int(line[3])]

    def draw_text(self, text, pos):
        font = pygame.font.Font(None, 40)
        text_surf = font.render(text, True, (0,0,0))
        self.win.blit(text_surf, ( pos[0]-text_surf.get_width()-10,
                                    pos[1]-text_surf.get_height()-10))

    def draw(self):
        self.win.blit(self.track, (0,0))

        for car in self.cars:
            car_surf = pygame.Surface((car.img.get_width(), car.img.get_height()))
            car_surf.set_colorkey((0,0,0))
            car_surf.fill((255,0,0))

            rotated_surf = pygame.transform.rotate(car_surf, car.angle)
            self.win.blit(rotated_surf, (car.x-rotated_surf.get_width()//2, car.y-rotated_surf.get_height()//2))

        self.draw_text(f"Generation: {self.generation}", (self.WIDTH, self.HEIGHT))

        pygame.display.update()

    def run_simulation(self, genomes, config):
        self.generation += 1

        nets = []
        ge = []

        for _, genome in genomes:
            genome.fitness = 0
            ge.append(genome)

            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)

            self.cars.append(Car(self.START_POS[0], self.START_POS[1]))

        clock = pygame.time.Clock()

        run = True 
       
        while run and len(self.cars)>0:
            clock.tick(0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                    pygame.quit()
                    exit()
                    
            for i, car in enumerate(self.cars):
                output = nets[i].activate(car.get_distances(self.track))
                # index of action that gives the best potential effect
                # 0 - rotate counterclockwise
                # 1 - rotate clockwise
                # 2 - brake
                x = output.index(max(output))
                if x == 0:
                    car.rotate(-1)
                elif x == 1:
                    car.rotate(1)
             
            for i, car in enumerate(self.cars):
                car.move()

                if car.collision(self.track):
                    nets.pop(i)
                    ge.pop(i)
                    self.cars.pop(i)
                else:
                    ge[i].fitness += car.get_reward()
                   
            self.draw()
            





