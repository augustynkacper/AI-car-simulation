import pygame 
from Intro import Intro
from Player import Player
from AICar import AICar
import neat
import os

pygame.init()

WIDTH, HEIGHT = 1100, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

def run():
    game_state = Intro(WIDTH, HEIGHT, win)

    while True:
        clock.tick(60)
        game_state = game_state.run()

        if game_state is None:
            break

if __name__ == "__main__":

    run()

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    car_simulation = AICar(WIDTH, HEIGHT, win)

    p.run(car_simulation.run_simulation, 20)

