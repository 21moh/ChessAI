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
                            # checks if move is possible from the move list
                            result = (game.board.grid[dragger.initial_row][dragger.initial_col].moves).count([clicked_row, clicked_col])        # checks for valid placement

                            
                            if (clicked_row < ROWS and clicked_col < COLS):
                                if (result >= 1):                           # player drops piece into valid square

                                    if (self.game.board.whiteInCheck == False):

                                        # check if moving the piece would lead to a check

                                        copygrid = copy.deepcopy(game.board.grid)
                                        saveinitial = copy.deepcopy(game.board.grid[dragger.initial_row][dragger.initial_col])
                                        copygrid[clicked_row][clicked_col] = saveinitial
                                        copygrid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                        game.board.loadProtections2(copygrid)
                                        inCheck = game.board.checkChecker("black", copygrid)

                                        if inCheck == False:
                                            if (game.board.grid[dragger.initial_row][dragger.initial_col].team == "white" and game.board.grid[clicked_row][clicked_col].team == "black"):   #capture for white
                                                
                                                if dragger.piece == "king":
                                                    
                                                    if game.board.grid[clicked_row][clicked_col].blackprotected == False:       # move for King

                                                        
                                                        game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                        game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                        game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                        game.board.grid[clicked_row][clicked_col].moves = []
                                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                        game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                        turn = "black"
                                                        game.board.whiteKingLoc = [clicked_row, clicked_col]
                                                        game.board.checkChecker("white", game.board.grid)

                                                else:               # move piece into empty square

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
                                                        game.board.checkChecker("white", game.board.grid)


                                
                                            elif game.board.grid[clicked_row][clicked_col].piece == None and game.board.grid[dragger.initial_row][dragger.initial_col].team == "white" and clicked_row < ROWS and clicked_col < COLS:
                                                #moving piece to empty square

                                                if dragger.piece == "king":
                                                    if game.board.grid[clicked_row][clicked_col].blackprotected == False:
                                                        game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                        game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                        game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                        game.board.grid[clicked_row][clicked_col].moves = []
                                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                        game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                        turn = "black"
                                                        game.board.whiteKingLoc = [clicked_row, clicked_col]
                                                        game.board.checkChecker("white", game.board.grid)



                                                else:
                                                    if dragger.piece.piece == "pond" and clicked_row == 0:     # transform pond into Queen
                                                        game.board.grid[clicked_row][clicked_col] = Square(clicked_row, clicked_col)
                                                        game.board.grid[clicked_row][clicked_col].add_piece("white", "queen", "images/whiteQueen.png", clicked_row, clicked_col)
                                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                        game.board.checkChecker("white", game.board.grid)
                                                        turn = "black"


                                                    else:
                                                        # copy all piece information into new Square and Piece
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
                                        
                                        print("WHITE IN CHECK")
                                        for i in range(len(game.board.white_movable)):
                                            if game.board.white_move[i][0] == clicked_row and game.board.white_move[i][1] == clicked_col:
                                                print("passed wall 1")
                                                x = game.board.white_move[i][0]
                                                y = game.board.white_move[i][1]
                                                print("move towards coords:", x,y)
                                                if clicked_row == x and clicked_col == y:
                                                    print("passed wall 2")
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

                            game.board.checkChecker("white", game.board.grid) #--> attacking from black
                            # checks if move is possible from the move list
                            result = (game.board.grid[dragger.initial_row][dragger.initial_col].moves).count([clicked_row, clicked_col])        # checks for valid placement

                            if (clicked_row < ROWS and clicked_col < COLS):
                                if (result >= 1):                           # player drops piece into valid square

                                    if (self.game.board.blackInCheck == False):
                                        copygrid = copy.deepcopy(game.board.grid)
                                        saveinitial = copy.deepcopy(game.board.grid[dragger.initial_row][dragger.initial_col])
                                        copygrid[clicked_row][clicked_col] = saveinitial
                                        copygrid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                        game.board.loadProtections2(copygrid)
                                        inCheck = game.board.checkChecker("white", copygrid)

                                        if inCheck == False:
                                            if (game.board.grid[dragger.initial_row][dragger.initial_col].team == "black" and game.board.grid[clicked_row][clicked_col].team == "white"):   #capture for black
                                                
                                                if dragger.piece == "king":
                                                    
                                                    if game.board.grid[clicked_row][clicked_col].whiteprotected == False:       # move for King

                                                        
                                                        game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                        game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                        game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                        game.board.grid[clicked_row][clicked_col].moves = []
                                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                        game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                        game.board.blackKingLoc = [clicked_row, clicked_col]
                                                        game.board.checkChecker("black", game.board.grid)
                                                        turn = "white"

                                                else:               # move piece into empty square

                                                    if dragger.piece.piece == "pond" and clicked_row == 0:     # transform pond into Queen
                                                        print("accessed")
                                                        game.board.grid[clicked_row][clicked_row].piece = "queen"
                                                        game.board.grid[clicked_row][clicked_col].team = "black"
                                                        game.board.grid[clicked_row][clicked_col].image = "images/blackQueen.png"
                                                        game.board.grid[clicked_row][clicked_col].moves = []
                                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                        game.board.checkChecker("black", game.board.grid)
                                                        turn = "white"
                                                    else:
                                                        # shift all piece information into new Square and Piece for capture
                                                        game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                        game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                        game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                        game.board.grid[clicked_row][clicked_col].moves = []
                                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                        game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                        game.board.checkChecker("black", game.board.grid)
                                                        turn = "white"


                                
                                            elif game.board.grid[clicked_row][clicked_col].piece == None and game.board.grid[dragger.initial_row][dragger.initial_col].team == "black" and clicked_row < ROWS and clicked_col < COLS:
                                                #moving piece to empty square

                                                if dragger.piece == "king":
                                                    if game.board.grid[clicked_row][clicked_col].whiteprotected == False:
                                                        game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                        game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                        game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                        game.board.grid[clicked_row][clicked_col].moves = []
                                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                        game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                        game.board.blackKingLoc = [clicked_row, clicked_col]
                                                        game.board.checkChecker("black", game.board.grid)
                                                        turn = "white"

                                                else:
                                                    print(dragger.piece.piece, clicked_row)
                                                    if dragger.piece.piece == "pond" and clicked_row == 0:     # transform pond into Queen
                                                        print("accessed")
                                                        game.board.grid[clicked_row][clicked_row].piece = "queen"
                                                        game.board.grid[clicked_row][clicked_col].team = "black"
                                                        game.board.grid[clicked_row][clicked_col].image = "images/blackQueen.png"
                                                        game.board.grid[clicked_row][clicked_col].moves = []
                                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                        game.board.checkChecker("black", game.board.grid)
                                                        turn = "white"

                                                    else:
                                                        # copy all piece information into new Square and Piece
                                                        game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                        game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                        game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                        game.board.grid[clicked_row][clicked_col].moves = []
                                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                        game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                        if dragger.piece == 'king':
                                                            game.board.blackKingLoc = [clicked_row, clicked_col]
                                                        game.board.checkChecker("black", game.board.grid)
                                                        turn = "white"

                                    elif (self.game.board.blackInCheck == True):
                                        
                                        print("BLACK IN CHECK")
                                        
                                        
                                        print("wall 0")
                                        print(game.board.black_movable)
                                        for i in range(len(game.board.black_movable)):
                                            if game.board.black_move[i][0] == clicked_row and game.board.black_move[i][1] == clicked_col:
                                                print("passed wall 1")
                                                x = game.board.black_move[i][0]
                                                y = game.board.black_move[i][1]
                                                print("move towards coords:", x,y)
                                                if clicked_row == x and clicked_col == y:
                                                    print("passed wall 2")
                                                    game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                    game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                    game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                    game.board.grid[clicked_row][clicked_col].moves = []
                                                    game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                    game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                    game.board.black_movable = []
                                                    game.board.black_move = []
                                                    turn = "white"
                                                    game.board.checkChecker("black", game.board.grid)
                                                    if dragger.piece.piece == "king":
                                                        game.board.blackKingLoc = [clicked_row, clicked_col]
                                            
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
