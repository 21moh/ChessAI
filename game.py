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


    def show_pieces(self, screen):
        board = self.board
        for i in range(ROWS):
            for j in range(COLS):
                if (board[i][j].hasPiece):
                    piece = board[i][j].
                    
                    original_image = pygame.image.load(piece.image)
                    original_width, original_height = original_image.get_size()

                    spacing_factor = 0.9

                    # Calculate the scaling factors
                    width_scale = CELL_SIZE * spacing_factor / original_width
                    height_scale = CELL_SIZE * spacing_factor / original_height

                    # Use the smaller scaling factor to maintain aspect ratio
                    scale_factor = min(width_scale, height_scale)

                    # Scale the image
                    piece.image = pygame.transform.scale(original_image, (int(original_width * scale_factor), int(original_height * scale_factor)))
    
