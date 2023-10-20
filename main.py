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
            
            #  if turn == white     ->> HUMAN SECTION  

        #############################################     WHITE          #################################################################################################################
            game.board.loadProtections()
            #game.board.printProtections()

            if self.game.board.whiteInCheckmate == True:
                img = pygame.image.load("images/black wins.png")
                screen.blit(img, (-50, 100))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            if self.game.board.blackInCheckmate == True:
                img = pygame.image.load("images/white wins.png")
                screen.blit(img, (-50, 100))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            
            elif turn == "white":

                if dragger.dragging == True:
                    clicked_row = dragger.mouseY // CELL_SIZE
                    clicked_col = dragger.mouseX // CELL_SIZE

                    # creates all possible move locations with piece
                    game.board.grid[dragger.initial_row][dragger.initial_col].moves = game.board.get_moves(dragger.piece.piece, dragger.initial_row, dragger.initial_col, dragger.piece.team, game.board.grid)
                    
                    #print(game.board.grid[dragger.initial_row][dragger.initial_col].moves)
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

                        if game.board.whiteInCheck == True:
                            for i in range(len(game.board.whiteBlocks)):
                                if game.board.grid[clicked_row][clicked_col] in game.board.whiteBlocks[i]:
                                    dragger.save_object(game.board.grid[clicked_row][clicked_col])
                                    dragger.save_initial(event.pos)
                                    dragger.drag_piece(game.board.grid[clicked_row][clicked_col])      
                                    break                                                           # gets specific piece on square 

                        
                        
                        elif game.board.whiteInCheck == False:
                            if game.board.grid[clicked_row][clicked_col].piece != None and game.board.grid[clicked_row][clicked_col].team == "white":         # or opponent piece condition
                                dragger.save_object(game.board.grid[clicked_row][clicked_col])
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(game.board.grid[clicked_row][clicked_col])        # gets specific piece on square 



                    if event.type == pygame.MOUSEBUTTONUP:
                        if dragger.piece != None:
                            clicked_row = dragger.mouseY // CELL_SIZE
                            clicked_col = dragger.mouseX // CELL_SIZE

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
                                                    game.board.checkChecker("white")

                                            else:               # move piece into empty square

                                                if dragger.piece.piece == "pond" and clicked_row == 0:     # transform pond into Queen
                                                    print("accessed")
                                                    game.board.grid[clicked_row][clicked_row].piece = "queen"
                                                    game.board.grid[clicked_row][clicked_col].team = "white"
                                                    game.board.grid[clicked_row][clicked_col].image = "images/whiteQueen.png"
                                                    game.board.grid[clicked_row][clicked_col].moves = []
                                                    game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                    game.board.checkChecker("white")
                                                else:
                                                    # shift all piece information into new Square and Piece for capture
                                                    game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                    game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                    game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                    game.board.grid[clicked_row][clicked_col].moves = []
                                                    game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                    game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                    turn = "black"
                                                    game.board.checkChecker("white")


                            
                                        elif game.board.grid[clicked_row][clicked_col].piece == None and game.board.grid[dragger.initial_row][dragger.initial_col].team == "white" and clicked_row < ROWS and clicked_col < COLS:

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
                                                    game.board.checkChecker("white")


                                            else:
                                                print(dragger.piece.piece, clicked_row)
                                                if dragger.piece.piece == "pond" and clicked_row == 0:     # transform pond into Queen
                                                    print("accessed")
                                                    game.board.grid[clicked_row][clicked_row].piece = "queen"
                                                    game.board.grid[clicked_row][clicked_col].team = "white"
                                                    game.board.grid[clicked_row][clicked_col].image = "images/whiteQueen.png"
                                                    game.board.grid[clicked_row][clicked_col].moves = []
                                                    game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                    game.board.checkChecker("white")


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
                                                    game.board.checkChecker("white")

                                    elif (self.game.board.whiteInCheck == True):
                                        
                                        print("WHITE IN CHECK")

                                        # board moves when in check need to be checked
                                        copylist = []               
                                        kinglist = []
                                        for i in range(len(game.board.whiteBlocks)):
                                            copylist.append(game.board.whiteBlocks[i][0])       #whiteblocks is list of [SquareObject, row to move, col to move]
                                        for i in range(len(game.board.whiteKingMoves)):
                                            kinglist.append(game.board.whiteKingMoves[i])       #whiteKingMoves is king's list of [row, col]


                                        if game.board.grid[dragger.initial_row][dragger.initial_col] in copylist or (dragger.piece == "king" and [clicked_row, clicked_col] in kinglist):
                                            if (game.board.grid[dragger.initial_row][dragger.initial_col] in copylist):
                                                for i in range(len(game.board.whiteBlocks)):
                                                    if game.board.whiteBlocks[i][0] == self.game.board.grid[dragger.initial_row][dragger.initial_col] and clicked_row == game.board.whiteBlocks[i][1] and clicked_col == game.board.whiteBlocks[i][2]:
                                                        
                                                        self.game.board.grid[clicked_row][clicked_col] = copylist[i]
                                                        game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                        game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                        game.board.grid[clicked_row][clicked_col].moves = []
                                                        game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                        game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                        turn = "black"
                                                        self.game.board.whiteInCheck = False
                                                        self.game.board.whiteBlocks = []
                                                        self.game.board.whiteKingMoves = []

                                                        if dragger.piece == 'king':
                                                            game.board.whiteKingLoc = [clicked_row, clicked_col]

                                                        game.board.checkChecker("white")
                                                        break
                                            
                                            elif (dragger.piece == "king" and [clicked_row, clicked_col] in kinglist):
                                    
                                                
                                                self.game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                game.board.grid[clicked_row][clicked_col].moves = []
                                                game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                turn = "black"
                                                self.game.board.whiteInCheck = False
                                                self.game.board.whiteBlocks = []
                                                self.game.board.whiteKingMoves = []

                                                if dragger.piece == 'king':
                                                    game.board.whiteKingLoc = [clicked_row, clicked_col]
                                                game.board.checkChecker("white")


                                        
                                        
                            dragger.dragging = False
                            dragger.piece = None
                            dragger.object = None
                            game.board.printProtections()


                
        ################################################    BLACK        ##############################################################################################################



            # if turn equals black --> AI SECTION
            elif turn == "black":


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
                            
                            game.board.checkChecker("black")

                            turn = "white"

                        else:

                            game.board.grid[movelist[selectMove][0]][movelist[selectMove][1]] = game.board.grid[index1][index2]
                            game.board.grid[index1][index2] = Square(index1, index2)
                            
                            game.board.checkChecker("black")

                            turn = "white"







                elif game.board.blackInCheck == True:
                    print("BLACK IN CHECK")
                    print(self.game.board.blackBlocks)
                    if (len(self.game.board.blackBlocks) > 0):
                        print(self.game.board.grid[self.game.board.blackBlocks[0][1]][self.game.board.blackBlocks[0][2]].piece)
                    if len(self.game.board.blackBlocks) > 0:       # move piece to block
                        moveChoice = random.randint(0,len(self.game.board.blackBlocks)-1)
                        move = self.game.board.blackBlocks[moveChoice]
                        copyobject = copy.deepcopy(move[0])

                        game.board.grid[move[1]][move[2]] = copyobject
                        game.board.grid[move[1]][move[2]].row = move[1]
                        game.board.grid[move[1]][move[2]].col = move[2]
                        game.board.grid[move[1]][move[2]].moves = []
                        game.board.grid[move[0].row][move[0].col] = Square(index1, index2)


                        self.game.board.blackInCheck = False
                        self.game.board.blackBlocks = []
                        self.game.board.blackKingMoves = []
                        game.board.checkChecker("black")
                        turn = "white"

                    else: # move king out of check
                        moveChoice = random.randint(0,len(game.board.blackKingMoves)-1)
                        move = self.game.board.blackKingMoves
                        kingMoved = False

                        for index in move:
                            if game.board.grid[index[0]][index[1]].whiteprotected == False:
                                game.board.grid[index[0]][index[1]] = game.board.grid[self.game.board.blackKingLoc[0]][self.game.board.blackKingLoc[1]]
                                game.board.grid[index[0]][index[1]].row = index[0]
                                game.board.grid[index[0]][index[1]].col = index[1]
                                game.board.grid[index[0]][index[1]].moves = []
                                game.board.grid[self.game.board.blackKingLoc[0]][self.game.board.blackKingLoc[1]] = Square(index1, index2)

                                game.board.blackKingLoc = [index[0], index[1]]

                                self.game.board.blackInCheck = False
                                self.game.board.blackBlocks = []
                                self.game.board.blackKingMoves = []
                                game.board.checkChecker("black")
                                turn = "white"
                                kingMoved = True
                                break

                        if kingMoved == False:
                            self.game.board.blackInCheckmate = True

                        

                        

                        
                        
                    


            pygame.display.flip()
    
    


    

main = Main()
main.mainloop()
