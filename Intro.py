import pygame
import sys
from Player import Player
from GameState import GameState

class Intro(GameState):

    def __init__(self, W, H, win):
        super().__init__(W, H, win)
        self.font = pygame.font.Font(None, 36)

    def display_text(self):
        player = self.font.render("Let me drive", True, (255,255,255))
        ai = self.font.render("Let AI take control", True, (255,255,255))

        plr_dim = (player.get_width(), player.get_height())
        ai_dim = (ai.get_width(), ai.get_height())

        self.win.blit(player, (self.WIDTH//4-plr_dim[0]//2, self.HEIGHT//2-plr_dim[1]//2))
        self.win.blit(ai, (3*self.WIDTH//4-ai_dim[0]//2, self.HEIGHT//2-ai_dim[1]//2))

    def highlight_choice(self):
        if pygame.mouse.get_focused()==0: return
        mouse_x = pygame.mouse.get_pos()[0]
        if mouse_x < self.WIDTH//2:
            x_pos = 0
        elif self.WIDTH//2 <= mouse_x:
            x_pos = self.WIDTH//2
        pygame.draw.rect(self.win, (25,25,25), (x_pos,0,self.WIDTH//2, self.HEIGHT))

    def draw(self):
        self.win.fill((0,0,0))
        self.highlight_choice()
        pygame.draw.line(self.win, (255,255,255), (self.WIDTH//2, 0), (self.WIDTH//2, self.HEIGHT))
        self.display_text()
        pygame.display.update()

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] < self.WIDTH//2:
                    return Player(self.WIDTH, self.HEIGHT, self.win)
   
        self.draw()
        return self