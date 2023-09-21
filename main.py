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
        dragger = self.game.dragger

        #initiate pygame
        #initialize board
        #draw board while running

        running = True

        while running:
            game.board.initialize_board()
            game.show_board(screen)
            game.show_pieces(screen)
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False  # Set the flag to exit the loop if the window is closed
                    pygame.quit()  # Quit Pygame properly
                    sys.exit()     # exit program quit game
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // CELL_SIZE
                    clicked_col = dragger.mouseX // CELL_SIZE

                    if game.board.grid[clicked_row][clicked_col].piece != None:
                        piece = game.board.grid[clicked_row][clicked_col].piece
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)

                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece


            pygame.display.update()


    

main = Main()
main.mainloop()
