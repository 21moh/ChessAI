import pygame
import sys

from const import *
from game import Game
from square import Square


class Main:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Chess')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #, pygame.HWSURFACE
        self.game = Game()

    def mainloop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger

        #initiate pygame
        #initialize board
        #draw board while running

        running = True
        game.board.initialize_board()



        while running:
            game.show_board(screen)
            game.show_pieces(screen)
            
            #  if turn == white     ->> HUMAN SECTION  

            if dragger.dragging == True:
                dragger.update_mouse(event.pos)
                dragger.update_blit(screen)


            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False  # Set the flag to exit the loop if the window is closed
                    pygame.quit()  # Quit Pygame properly
                    sys.exit()     # exit program quit game
                
                

                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // CELL_SIZE
                    clicked_col = dragger.mouseX // CELL_SIZE

                    if game.board.grid[clicked_row][clicked_col].piece != None:         # or opponent piece condition
                        dragger.save_object(game.board.grid[clicked_row][clicked_col])
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(game.board.grid[clicked_row][clicked_col])        # gets specific piece on square 
                        #dragger.hover()


                if event.type == pygame.MOUSEMOTION:
                    pass
                    
                    #if dragger.dragging == True:
                    #    dragger.update_mouse(event.pos)
                    #    dragger.update_blit(screen)




                if event.type == pygame.MOUSEBUTTONUP:
                    dragger.dragging = False
                    dragger.piece = None
                    dragger.object = None
                    # check for valid move:

                    #if valid move -->
                    clicked_row = dragger.mouseY // CELL_SIZE
                    clicked_col = dragger.mouseX // CELL_SIZE
                    if (clicked_row < ROWS and clicked_col < COLS):
                        if game.board.grid[clicked_row][clicked_col].piece == None and clicked_row < ROWS and clicked_col < COLS:

                            # check if move is valid
                            game.board.grid[dragger.initial_row][dragger.initial_col].get_moves()               # gets all possible moves for piece
                            possible_moves = game.board.grid[dragger.initial_row][dragger.initial_col].moves    # returns list of all possible moves for piece
                            result = possible_moves.count([clicked_row, clicked_col])
                            print(possible_moves)
                            print(result)
                            if result >= 1:

                                # put clicked object in new location
                                

                                # copy all piece information into new Square and Piece
                                game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                game.board.grid[clicked_row][clicked_col].row = clicked_row
                                game.board.grid[clicked_row][clicked_col].col = clicked_col
                                game.board.grid[clicked_row][clicked_col].moves = []
                                game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)

                        

                                print(game.board.grid[clicked_row][clicked_col].piece)
                                
                                game.show_board(screen)
                                game.show_pieces(screen)

                            game.board.grid[dragger.initial_row][dragger.initial_col].moves = []




            # if turn equals black --> AI SECTION


            pygame.display.flip()


    

main = Main()
main.mainloop()
