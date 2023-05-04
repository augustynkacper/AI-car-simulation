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
        self.track = pygame.transform.scale(pygame.image.load("track.png"), (W,H))
        self.best = self.read_best()
        self.generation = 0

    def read_best(self):
        file = open("best.txt", "r")
        line = file.readline()
        line = line.split(" ")
        return [int(line[1]), int(line[2]), int(line[3])]


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
            clock.tick(60)

            
        




