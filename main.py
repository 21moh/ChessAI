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

            
            #  if turn == white     ->> HUMAN SECTION  

        #############################################     WHITE          #################################################################################################################
            #game.board.printProtections()
            
            if turn == "white":

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

                            game.board.checkChecker("black", game.board.grid) #--> attacking from black
                            # checks if move is possible from the move list
                            result = (game.board.grid[dragger.initial_row][dragger.initial_col].moves).count([clicked_row, clicked_col])        # checks for valid placement

                            if (clicked_row < ROWS and clicked_col < COLS):
                                if (result >= 1):                           # player drops piece into valid square

                                    if (self.game.board.whiteInCheck == False):
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
                                                    print("accessed")
                                                    game.board.grid[clicked_row][clicked_row].piece = "queen"
                                                    game.board.grid[clicked_row][clicked_col].team = "white"
                                                    game.board.grid[clicked_row][clicked_col].image = "images/whiteQueen.png"
                                                    game.board.grid[clicked_row][clicked_col].moves = []
                                                    game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                    game.board.checkChecker("white", game.board.grid)
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
                                                print(dragger.piece.piece, clicked_row)
                                                if dragger.piece.piece == "pond" and clicked_row == 0:     # transform pond into Queen
                                                    print("accessed")
                                                    game.board.grid[clicked_row][clicked_row].piece = "queen"
                                                    game.board.grid[clicked_row][clicked_col].team = "white"
                                                    game.board.grid[clicked_row][clicked_col].image = "images/whiteQueen.png"
                                                    game.board.grid[clicked_row][clicked_col].moves = []
                                                    game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                    game.board.checkChecker("white", game.board.grid)


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

                                    elif (self.game.board.whiteInCheck == True):
                                        
                                        print("WHITE IN CHECK")
                                        game.board.InCheckMoves("white")
                                        if (self.whiteInCheckmate == True):
                                            img = pygame.image.load("images/black wins.png")
                                            screen.blit(img, (-50, 100))
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    sys.exit()
                                        else:
                                            if game.board.grid[dragger.initial_row][dragger.initial_col] in game.board.white_movable:
                                                if [clicked_row, clicked_col] in game.board.move:
                                                    game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                    game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                    game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                    game.board.grid[clicked_row][clicked_col].moves = []
                                                    game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                    game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                    turn = "black"
                                                    if dragger.piece == 'king':
                                                        game.board.whiteKingLoc = [clicked_row, clicked_col]
                                                    game.board.whiteInCheck = False
                                                    game.board.white_movable = []
                                                    game.board.white_move = []
                                                    game.board.checkChecker("white", game.board.grid)

                                        


                                        
                                        
                            dragger.dragging = False
                            dragger.piece = None
                            dragger.object = None
                            game.board.printProtections()


                
        ################################################    BLACK        ##############################################################################################################



            # if turn equals black --> AI SECTION
            elif turn == "black":
                
                game.board.checkChecker("white", game.board.grid)


                if game.board.blackInCheck == False:
                    index1 = random.randint(0,7)
                    index2 = random.randint(0,7)
                    if game.board.grid[index1][index2].team == "black":
                        game.board.grid[index1][index2].moves = game.board.get_moves(game.board.grid[index1][index2].piece, index1, index2, "black", game.board.grid)
                        movelist = game.board.grid[index1][index2].moves
                        while (len(movelist) == 0):
                            index1 = random.randint(0,7)
                            index2 = random.randint(0,7)
                            if game.board.grid[index1][index2].team == "black":
                                game.board.grid[index1][index2].moves = game.board.get_moves(game.board.grid[index1][index2].piece, index1, index2, "black", game.board.grid)
                                movelist = game.board.grid[index1][index2].moves
                        selectMove = random.randint(0, len(movelist)-1)



                       # print("white locs:")
                       # print(self.game.board.white_locs)
                       # print("black locs")
                       # print(self.game.board.black_locs)


                        if game.board.grid[index1][index2].piece == 'king':
                            game.board.blackKingLoc = [movelist[selectMove][0], movelist[selectMove][1]]

                            game.board.grid[movelist[selectMove][0]][movelist[selectMove][1]] = game.board.grid[index1][index2]
                            if (game.board.grid[index1][index2].whiteprotected == False):
                                game.board.grid[index1][index2] = Square(index1, index2)
                            
                            turn = "white"

                        else:

                            game.board.grid[movelist[selectMove][0]][movelist[selectMove][1]] = game.board.grid[index1][index2]
                            game.board.grid[index1][index2] = Square(index1, index2)
                            
                            turn = "white"







                elif game.board.blackInCheck == True:
                    print("BLACK IN CHECK")

                    game.board.InCheckMoves("black")
                    if game.board.blackInCheckmate == True:
                        img = pygame.image.load("images/white wins.png")
                        screen.blit(img, (-50, 100))
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                    else:
                        print("THIS IS ACCESSED")
                        print("=====INFO=====")
                        game.board.printProtections()
                        print(game.board.black_move)
                        for i in range(len(game.board.black_movable)):
                            print("Black movable pieces:", game.board.black_movable[i].piece)
                        print(len(game.board.black_movable))
                        print(len(game.board.black_move))
                        index = random.randint(0,len(game.board.black_move)-1)
                        game.board.grid[game.board.black_move[index][0]][game.board.black_move[index][1]] = game.board.black_movable[index]
                        row = game.board.black_movable[index].row
                        col = game.board.black_movable[index].col
                        game.board.grid[row][col] = Square(row, col)
                        game.board.grid[game.board.black_move[index][0]][game.board.black_move[index][1]].row = game.board.black_move[index][0]
                        game.board.grid[game.board.black_move[index][0]][game.board.black_move[index][1]].col = game.board.black_move[index][1]
                        game.board.grid[game.board.black_move[index][0]][game.board.black_move[index][1]].moves = []
                        if dragger.piece == "king":
                            game.board.blackKingLoc = [game.board.black_move[index][0], game.board.black_move[index][1]]

                        game.board.blackInCheck = False
                        game.board.black_move = []
                        game.board.black_movable = []
                        turn = "white"
                    

                    
                    


            pygame.display.flip()
    
    


    

main = Main()
main.mainloop()
