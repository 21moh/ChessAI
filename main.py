import pygame
import sys
import random
import copy

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
        printed = False

        while running:
            game.show_board(screen)
            game.show_pieces(screen)
            game.board.loadProtections()


            if (self.game.board.blackInCheckmate == True):
                img = pygame.image.load("images/white wins.png")
                screen.blit(img, (-50, 100))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            if (self.game.board.whiteInCheckmate == True):
                img = pygame.image.load("images/black wins.png")
                screen.blit(img, (-50, 100))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            
            #  if turn == white     ->> HUMAN SECTION  

        #############################################     WHITE          #################################################################################################################
            #game.board.printProtections()
            
            if turn == "white":

                if dragger.dragging == True:
                    
                    print(dragger.piece.piece)

                    clicked_row = dragger.mouseY // CELL_SIZE
                    clicked_col = dragger.mouseX // CELL_SIZE
                    # creates all possible move locations with piece
                    game.board.grid[dragger.initial_row][dragger.initial_col].moves = game.board.get_moves(dragger.piece.piece, dragger.initial_row, dragger.initial_col, dragger.piece.team, game.board.grid)
                    
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
                        dragger.save_object(game.board.grid[clicked_row][clicked_col])
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(game.board.grid[clicked_row][clicked_col])        # gets specific piece on square 

                    if event.type == pygame.MOUSEBUTTONUP:
                        if dragger.piece != None:
                            clicked_row = dragger.mouseY // CELL_SIZE
                            clicked_col = dragger.mouseX // CELL_SIZE

                            game.board.checkChecker("black", game.board.grid) #--> attacking from black

                            
                            directions = game.board.CanCastle("white")
                            if len(directions) > 0:
                                if dragger.piece.piece == "king" and dragger.initial_row == 7 and dragger.initial_col == 4 and clicked_row == 7 and clicked_col == 7:
                                    game.board.Castle("white", "right")
                                    game.board.checkChecker("white", game.board.grid)
                                    turn = "black"
                                elif dragger.piece.piece == "king" and dragger.initial_row == 7 and dragger.initial_col == 4 and clicked_row == 7 and clicked_col == 0:
                                    game.board.Castle("white", "left")
                                    game.board.checkChecker("white", game.board.grid)
                                    turn = "black"


                            # checks if move is possible from the move list
                            result = (game.board.grid[dragger.initial_row][dragger.initial_col].moves).count([clicked_row, clicked_col])        # checks for valid placement

                            
                            if (clicked_row < ROWS and clicked_col < COLS and turn == "white"):
                                if (result >= 1):                           # player drops piece into valid square

                                    if (self.game.board.whiteInCheck == False):

                                        copygrid = copy.deepcopy(game.board.grid)
                                        saveinitial = copy.deepcopy(game.board.grid[dragger.initial_row][dragger.initial_col])
                                        copygrid[clicked_row][clicked_col] = saveinitial
                                        copygrid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                        game.board.loadProtections2(copygrid)
                                        inCheck = game.board.checkChecker("black", copygrid)

                                        if inCheck == False:    # boolean prevents moving a friendly piece towards opening a check towards white king

                                            if dragger.piece.piece == "pond" and clicked_row == 0:     # transform pond into Queen
                                                game.board.grid[clicked_row][clicked_col] = Square(clicked_row, clicked_col)
                                                game.board.grid[clicked_row][clicked_col].add_piece("white", "queen", "images/whiteQueen.png", clicked_row, clicked_col)
                                                game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                game.board.checkChecker("white", game.board.grid)
                                                turn = "black"

                                            else:
                                                # shift all piece information into new Square and Piece for capture
                                                game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                game.board.grid[clicked_row][clicked_col].moves = []
                                                game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                turn = "black"
                                                if dragger.piece == 'king':
                                                    game.board.whiteKingLoc = [clicked_row, clicked_col]
                                                game.board.checkChecker("white", game.board.grid)
                                                        
                                    elif (self.game.board.whiteInCheck == True):
                                        for i in range(len(game.board.white_movable)):
                                            if game.board.white_move[i][0] == clicked_row and game.board.white_move[i][1] == clicked_col:
                                                x = game.board.white_move[i][0]
                                                y = game.board.white_move[i][1]
                                                if clicked_row == x and clicked_col == y:
                                                    game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                    game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                    game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                    game.board.grid[clicked_row][clicked_col].moves = []
                                                    game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                    game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                    game.board.white_movable = []
                                                    game.board.white_move = []
                                                    turn = "black"
                                                    game.board.checkChecker("white", game.board.grid)
                                                    if dragger.piece.piece == "king":
                                                        game.board.whiteKingLoc = [clicked_row, clicked_col]
                                            
                                                    break

                            dragger.dragging = False
                            dragger.piece = None
                            dragger.object = None
                            game.board.loadProtections()
                            if game.board.blackInCheck == True:
                                game.board.InCheckMoves("black")

                            


                
        ################################################    BLACK        ##############################################################################################################



            # if turn equals black --> AI SECTION
            elif turn == "black":

                if dragger.dragging == True:
                    
                    print(dragger.piece.piece)

                    clicked_row = dragger.mouseY // CELL_SIZE
                    clicked_col = dragger.mouseX // CELL_SIZE
                    # creates all possible move locations with piece
                    game.board.grid[dragger.initial_row][dragger.initial_col].moves = game.board.get_moves(dragger.piece.piece, dragger.initial_row, dragger.initial_col, dragger.piece.team, game.board.grid)
                    
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
                        dragger.save_object(game.board.grid[clicked_row][clicked_col])
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(game.board.grid[clicked_row][clicked_col])        # gets specific piece on square 

                    if event.type == pygame.MOUSEBUTTONUP:
                        if dragger.piece != None:
                            clicked_row = dragger.mouseY // CELL_SIZE
                            clicked_col = dragger.mouseX // CELL_SIZE

                            game.board.checkChecker("black", game.board.grid) 

                            
                            directions = game.board.CanCastle("black")
                            if len(directions) > 0:
                                if dragger.piece.piece == "king" and dragger.initial_row == 0 and dragger.initial_col == 4 and clicked_row == 0 and clicked_col == 7:
                                    game.board.Castle("black", "right")
                                    game.board.checkChecker("black", game.board.grid)
                                    turn = "white"
                                elif dragger.piece.piece == "king" and dragger.initial_row == 0 and dragger.initial_col == 4 and clicked_row == 0 and clicked_col == 0:
                                    game.board.Castle("black", "left")
                                    game.board.checkChecker("black", game.board.grid)
                                    turn = "white"


                            # checks if move is possible from the move list
                            result = (game.board.grid[dragger.initial_row][dragger.initial_col].moves).count([clicked_row, clicked_col])        # checks for valid placement

                            
                            if (clicked_row < ROWS and clicked_col < COLS and turn == "black"):
                                if (result >= 1):                           # player drops piece into valid square

                                    if (self.game.board.whiteInCheck == False):

                                        copygrid = copy.deepcopy(game.board.grid)
                                        saveinitial = copy.deepcopy(game.board.grid[dragger.initial_row][dragger.initial_col])
                                        copygrid[clicked_row][clicked_col] = saveinitial
                                        copygrid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                        game.board.loadProtections2(copygrid)
                                        inCheck = game.board.checkChecker("white", copygrid)

                                        if inCheck == False:    # boolean prevents moving a friendly piece towards opening a check towards white king

                                            if dragger.piece.piece == "pond" and clicked_row == 0:     # transform pond into Queen
                                                game.board.grid[clicked_row][clicked_col] = Square(clicked_row, clicked_col)
                                                game.board.grid[clicked_row][clicked_col].add_piece("white", "queen", "images/whiteQueen.png", clicked_row, clicked_col)
                                                game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                game.board.checkChecker("black", game.board.grid)
                                                turn = "black"

                                            else:
                                                # shift all piece information into new Square and Piece for capture
                                                game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                game.board.grid[clicked_row][clicked_col].moves = []
                                                game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                turn = "black"
                                                if dragger.piece == 'king':
                                                    game.board.whiteKingLoc = [clicked_row, clicked_col]
                                                game.board.checkChecker("black", game.board.grid)
                                                        
                                    elif (self.game.board.whiteInCheck == True):
                                        
                                        for i in range(len(game.board.white_movable)):
                                            if game.board.white_move[i][0] == clicked_row and game.board.white_move[i][1] == clicked_col:
                                                x = game.board.white_move[i][0]
                                                y = game.board.white_move[i][1]
                                                if clicked_row == x and clicked_col == y:
                                                    game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                    game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                    game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                    game.board.grid[clicked_row][clicked_col].moves = []
                                                    game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                    game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                    game.board.white_movable = []
                                                    game.board.white_move = []
                                                    turn = "black"
                                                    game.board.checkChecker("black", game.board.grid)
                                                    if dragger.piece.piece == "king":
                                                        game.board.whiteKingLoc = [clicked_row, clicked_col]
                                            
                                                    break

                            dragger.dragging = False
                            dragger.piece = None
                            dragger.object = None
                            game.board.loadProtections()
                            if game.board.whiteInCheck == True:
                                game.board.InCheckMoves("white")



                
                    

                    
                    


            pygame.display.flip()
    
    


    

main = Main()
main.mainloop()
