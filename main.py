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
                    game.board.grid[dragger.initial_row][dragger.initial_col].moves = game.board.get_moves(dragger.piece.piece, dragger.initial_row, dragger.initial_col, dragger.piece.team, game.board.grid)
                    
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
                            result = (game.board.grid[dragger.initial_row][dragger.initial_col].moves).count([clicked_row, clicked_col])        # checks for valid placement

                            if (clicked_row < ROWS and clicked_col < COLS):
                                if (result >= 1):                           # player drops piece into valid square


                                    # check if current King would be in check due to moved piece --> if it is, dont move the piece

                                    # if (kingInCheck() --> function uses a created copy board with piece in new place hypothetically) --> uses get_moves function inside the function for ALL pieces.

                                    # checks if moving the piece would reveal a check
                                    #copygrid = copy.deepcopy(game.board.grid)
                                    #temp = copy.deepcopy(game.board.grid[dragger.initial_row][dragger.initial_col])
                                    #copygrid[clicked_row][clicked_col] = temp
                                    #copygrid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                    

                                    #inCheck = game.board.check4Checks(copygrid, "white")
                                    #if inCheck == False:    # checks if move is allowed

                                    

                                        if (game.board.grid[dragger.initial_row][dragger.initial_col].team == "white" and game.board.grid[clicked_row][clicked_col].team == "black"):   #capture from white
                                            
                                            # update piece location in location map
                                            copyinitialrow = dragger.initial_row
                                            copyinitialcol = dragger.initial_col
                                            attacking_piece = game.board.grid[dragger.initial_row][dragger.initial_col].piece
                                            captured_piece = game.board.grid[clicked_row][clicked_col].piece
                                            self.game.board.white_locs[attacking_piece].remove((copyinitialrow, copyinitialcol)) 
                                            self.game.board.black_locs[captured_piece].remove((clicked_row, clicked_col))
                                            self.game.board.white_locs[attacking_piece].append((clicked_row, clicked_col))
                                            
                                            # copy all piece information into new Square and Piece
                                            game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                            game.board.grid[clicked_row][clicked_col].row = clicked_row
                                            game.board.grid[clicked_row][clicked_col].col = clicked_col
                                            game.board.grid[clicked_row][clicked_col].moves = []
                                            game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)

                                            game.board.grid[dragger.initial_row][dragger.initial_col].moves = []

                                            #get_moves
                                            turn = "black"


                            

                                        if game.board.grid[clicked_row][clicked_col].piece == None and game.board.grid[dragger.initial_row][dragger.initial_col].team == "white" and clicked_row < ROWS and clicked_col < COLS:

                                            # check if move is valid
                                            
                                            #print(result)

                                            copyinitialrow = dragger.initial_row
                                            copyinitialcol = dragger.initial_col
                                            attacking_piece = game.board.grid[dragger.initial_row][dragger.initial_col].piece

                                            self.game.board.white_locs[attacking_piece].remove((copyinitialrow, copyinitialcol)) 
                                            self.game.board.white_locs[attacking_piece].append((clicked_row, clicked_col))

                                            # copy all piece information into new Square and Piece
                                            game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                            game.board.grid[clicked_row][clicked_col].row = clicked_row
                                            game.board.grid[clicked_row][clicked_col].col = clicked_col
                                            game.board.grid[clicked_row][clicked_col].moves = []
                                            game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)

                                    

                                            #print(game.board.grid[clicked_row][clicked_col].piece)
                                            

                                            game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                            turn = "black"

                            dragger.dragging = False
                            dragger.piece = None
                            dragger.object = None


                
        ################################################    BLACK        ##############################################################################################################



            # if turn equals black --> AI SECTION
            elif turn == "black":
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


                    piece = game.board.grid[index1][index2].piece
                    self.game.board.black_locs[piece].remove((index1, index2)) 
                    if (game.board.grid[movelist[selectMove][0]][movelist[selectMove][1]].piece != None):
                        #checker = self.game.board.white_locs[game.board.grid[dragger.initial_row][dragger.initial_col].piece].count((clicked_row, clicked_col))
                        #if checker == 1:
                        self.game.board.white_locs[game.board.grid[movelist[selectMove][0]][movelist[selectMove][1]].piece].remove((movelist[selectMove][0], movelist[selectMove][1]))
                    self.game.board.black_locs[piece].append((movelist[selectMove][0], movelist[selectMove][1]))

                    print("white locs:")
                    print(self.game.board.white_locs)
                    print("black locs")
                    print(self.game.board.black_locs)

                    game.board.grid[movelist[selectMove][0]][movelist[selectMove][1]] = game.board.grid[index1][index2]
                    game.board.grid[index1][index2] = Square(index1, index2)
                    turn = "white"


            pygame.display.flip()


    

main = Main()
main.mainloop()
