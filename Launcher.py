import pygame 
from Car import Car
from GameState import GameState
from Intro import Intro

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

def run():
    
    game_state = Intro(WIDTH, HEIGHT, win)

    while True:
        clock.tick(60)
        game_state = game_state.run()


run()