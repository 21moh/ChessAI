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

        turn = "white"

        while running:
            game.show_board(screen)
            game.show_pieces(screen)
            
            #  if turn == white     ->> HUMAN SECTION  

        #############################################     WHITE          #################################################################################################################
            
            if turn == "white":

                if dragger.dragging == True:
                    clicked_row = dragger.mouseY // CELL_SIZE
                    clicked_col = dragger.mouseX // CELL_SIZE

                    # creates all possible move locations with piece
                    game.board.grid[dragger.initial_row][dragger.initial_col].moves = game.board.get_moves(dragger.piece.piece, dragger.initial_row, dragger.initial_col, dragger.piece.team)
                    
                    print(game.board.grid[dragger.initial_row][dragger.initial_col].moves)
                    # load all possible locations the piece can be placed
                    
                    game.board.loadPlacements(game.board.grid[dragger.initial_row][dragger.initial_col].moves, turn, screen)

                    
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

                        if game.board.grid[clicked_row][clicked_col].piece != None and game.board.grid[clicked_row][clicked_col].team == "white":         # or opponent piece condition
                            dragger.save_object(game.board.grid[clicked_row][clicked_col])
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(game.board.grid[clicked_row][clicked_col])        # gets specific piece on square 



                    if event.type == pygame.MOUSEBUTTONUP:
                        if dragger.piece != None:
                            clicked_row = dragger.mouseY // CELL_SIZE
                            clicked_col = dragger.mouseX // CELL_SIZE

                            # creates all possible move locations with piece
                            #game.board.grid[dragger.initial_row][dragger.initial_col].moves = game.board.get_moves(dragger.piece.piece, dragger.initial_row, dragger.initial_col, dragger.piece.team)
                            

                                    
                            print(game.board.grid[dragger.initial_row][dragger.initial_col].moves)

                            #implement move refiner --> checks for blocked moves in the list

                            # checks if move is possible from the move list
                            result = (game.board.grid[dragger.initial_row][dragger.initial_col].moves).count([clicked_row, clicked_col])

                            if (clicked_row < ROWS and clicked_col < COLS):
                                if (result >= 1):                           # player drops piece into valid square
                                    if (game.board.grid[dragger.initial_row][dragger.initial_col].team == "white" and game.board.grid[clicked_row][clicked_col].team == "black"):   #capture from white
                                        game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                        game.board.grid[clicked_row][clicked_col].row = clicked_row
                                        game.board.grid[clicked_row][clicked_col].col = clicked_col
                                        game.board.grid[clicked_row][clicked_col].moves = []
                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)

                                        game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                        turn = "black"


                        

                                    if game.board.grid[clicked_row][clicked_col].piece == None and game.board.grid[dragger.initial_row][dragger.initial_col].team == "white" and clicked_row < ROWS and clicked_col < COLS:

                                        # check if move is valid
                                        
                                        print(result)


                                        # copy all piece information into new Square and Piece
                                        game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                        game.board.grid[clicked_row][clicked_col].row = clicked_row
                                        game.board.grid[clicked_row][clicked_col].col = clicked_col
                                        game.board.grid[clicked_row][clicked_col].moves = []
                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)

                                

                                        print(game.board.grid[clicked_row][clicked_col].piece)
                                        

                                        game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                        turn = "black"

                            dragger.dragging = False
                            dragger.piece = None
                            dragger.object = None


                
        ################################################    BLACK        ##############################################################################################################



            # if turn equals black --> AI SECTION
            elif turn == "black":

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



                    if event.type == pygame.MOUSEBUTTONUP:
                        if dragger.piece != None:
                            clicked_row = dragger.mouseY // CELL_SIZE
                            clicked_col = dragger.mouseX // CELL_SIZE

                            # creates all possible move locations with piece
                            game.board.grid[dragger.initial_row][dragger.initial_col].moves = game.board.get_moves(dragger.piece.piece, dragger.initial_row, dragger.initial_col, dragger.piece.team)
                            

                                    
                            print(game.board.grid[dragger.initial_row][dragger.initial_col].moves)

                            #implement move refiner --> checks for blocked moves in the list

                            # checks if move is possible from the move list
                            result = (game.board.grid[dragger.initial_row][dragger.initial_col].moves).count([clicked_row, clicked_col])

                            if (clicked_row < ROWS and clicked_col < COLS):
                                if (result >= 1):                           # player drops piece into valid square
                                    if (game.board.grid[dragger.initial_row][dragger.initial_col].team == "black" and game.board.grid[clicked_row][clicked_col].team == "white"):   #capture from white
                                        game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                        game.board.grid[clicked_row][clicked_col].row = clicked_row
                                        game.board.grid[clicked_row][clicked_col].col = clicked_col
                                        game.board.grid[clicked_row][clicked_col].moves = []
                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)

                                        game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                        turn = "white"


                                    if game.board.grid[clicked_row][clicked_col].piece == None and game.board.grid[dragger.initial_row][dragger.initial_col].team == "black" and clicked_row < ROWS and clicked_col < COLS:

                                        # check if move is valid
                                        
                                        print(result)


                                        # copy all piece information into new Square and Piece
                                        game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                        game.board.grid[clicked_row][clicked_col].row = clicked_row
                                        game.board.grid[clicked_row][clicked_col].col = clicked_col
                                        game.board.grid[clicked_row][clicked_col].moves = []
                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)

                                

                                        print(game.board.grid[clicked_row][clicked_col].piece)
                                        

                                        game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                        turn = "white"


                            dragger.dragging = False
                            dragger.piece = None
                            dragger.object = None


            pygame.display.flip()


    

main = Main()
main.mainloop()
