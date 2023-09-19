import pygame
import sys

from const import *
from board import Board

class Game:
    def __init__(self):
        self.turn = "White"
        self.board = Board()
        #self.dragger = Dragger()
    
    def show_board(self, screen):
        
        screen.fill((200, 200, 200))  # White background

        # Draw the grid and pieces
        for row in range(8):
            for col in range(8):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
    