import pygame
import sys

from const import *
from game import Game

class Main:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Chess')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()

    def mainloop(self):
        game = self.game
        screen = self.screen

        #initiate pygame
        #initialize board
        #draw board while running

        running = True

        while running:
            game.show_board(screen)
            for event in pygame.event.get():
                pass
            pygame.display.update()


    

main = Main()
main.mainloop()