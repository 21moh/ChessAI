import pygame
import sys
import random
import copy

from const import *
from game import Game
from square import Square

import threading
import queue

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

        #draw board while running

        running = True
        game.board.initialize_board()

        turn = "white"

        
        #################################################################################################################################
        # Move Generator Section for Black AI
        # The function is placed outside the while loop because each while loop generates the graphics and the current position of all the pieces on the board. 
        # Thus, any delay to the main while loop's next iteration would cause a dropped white pieces to freeze due to the sequential algorithm for black finding its move.
        # Thus, threading is used so the the while loop can continue iterating without delay while the 'findMoveBlack' algorithm finds the best move for black.
        # When the findMoveBlack algorithm does finds the best move, the main while loop updates the board with the move found.
    
        
        q = queue.Queue()
        thread1 = None
        # for AI
        def findMoveBlack(game, q):
            grid = game.board.grid
            allmoves = dict()
            
            #recursive function which stores results in a dictionary
            def bestMove(grid, board, depth, allmoves, pts, moves):  
                if depth >= 2 or board.whiteInCheckmate == True:
                    #print("BASE CASE REACHED, DEPTH =", depth, "| White in checkmate:", board.whiteInCheckmate, "| Points from moves:", pts)
                    #print("MOVES:", moves)
                    if pts not in allmoves:
                        allmoves[pts] = []
                    allmoves[pts].append(moves)
                    return
                else:
                    Board = copy.deepcopy(board)
                    print("depth checker:", depth)
                    print("num points:", pts)
                    Board.postAttackers()
                    Board.loadPoints()
                    for loc in Board.blackPieces:
                        row = loc[0]
                        col = loc[1]
                        if grid[row][col].team == "black":
                            pieceMoves = Board.get_moves(grid[row][col].piece, row, col, "black", grid)
                            for move in pieceMoves:
                                Board2 = copy.deepcopy(Board)
                                tempPts = copy.copy(pts)
                                # check if piece is being attacked aka add defensive conditionals

                                if grid[move[0]][move[1]].whiteprotected == True:
                                    tempPts -= grid[row][col].points
                                if grid[move[0]][move[1]].team == "white":
                                    tempPts += grid[move[0]][move[1]].points
                                    if (depth == 0 and grid[move[0]][move[1]].piece == "queen"):
                                        tempPts += 20
                                if grid[move[0]][move[1]].piece != None and grid[move[0]][move[1]].whiteprotected == False:
                                    tempPts += grid[move[0]][move[1]].points                # Change, no change to tempPts
                                if grid[row][col].piece == "pond" and grid[move[0]][move[1]].team == "black" and len(grid[move[0]][move[1]].whiteAttackers) >= 1:
                                    arow = grid[move[0]][move[1]].whiteAttackers[0][0]
                                    acol= grid[move[0]][move[1]].whiteAttackers[0][1]
                                    tempPts += grid[arow][acol].points
                                Moves = copy.deepcopy(moves)
                                Moves.append([row, col, move[0], move[1]])
                                copyDepth = copy.deepcopy(depth)
                                if Board2.grid[move[0]][move[1]].team == "white":
                                    print("captured white hypothetical piece:", Board2.grid[move[0]][move[1]].piece, "| points gained from piece:", Board2.grid[move[0]][move[1]].points)
                                    print("moveset:", Moves)
                                    print("points gained", pts, "| in depth:", depth)

                                print("Recursion moves:", Moves)

                                save = copy.deepcopy(Board2.grid[row][col])
                                #print("all black piece locations:", Board2.blackPieces)
                                Board2.blackPieces.remove([row, col])
                                Board2.blackPieces.append([move[0], move[1]])
                                if Board2.grid[move[0]][move[1]].whiteprotected == True:
                                    Board2.blackPieces.remove([move[0], move[1]])
                                Board2.grid[move[0]][move[1]] = save
                                Board2.grid[move[0]][move[1]].row = move[0]
                                Board2.grid[move[0]][move[1]].col = move[1]
                                Board2.grid[row][col] = Square(row, col)
                                Board2.checkChecker("white", Board.grid)
                                if Board2.whiteInCheck:
                                    Board2.InCheckMoves("white")
                                #if depth <= 5:
                                copyDepth += 1
                                if tempPts >= 0:
                                    bestMove(Board2.grid, Board2, copyDepth, allmoves, tempPts, Moves)

            bestMove(game.board.grid, game.board, 0, allmoves, 0, [])
            game.board.printProtections()
            q.put(allmoves)


        def findCheckMoveBlack(game, moves, q):
            bestMove = None
            bestPoints = 0
            grid = game.board.grid
            for move in moves:
                Board = copy.deepcopy(game.board)
                capturePts = 0
                grid = Board.grid
                irow = move[0]
                icol = move[1]
                frow = move[2]
                fcol = move[3]
                initial = copy.deepcopy(grid[irow][icol])
                final = copy.deepcopy(grid[frow][fcol])

                if (final.whiteprotected == True):
                    capturePts += final.points
                    capturePts -= initial.points
                elif (final.whiteprotected == False):
                    capturePts += final.points
                if capturePts > bestPoints:
                    bestMove = move
            q.put(bestMove)
                

                
                


        #################################################################################################################################


        animating = False    # boolean for Black piece movement

        initial_row = None      # row and col for double list
        initial_col = None
        final_row = None
        final_col = None


        initial_x = None        # x and y like on a regular graph
        initial_y = None
        final_x = None
        final_y = None


        xIncrementer = 0        # incrementer values to move object across the board
        yIncrementer = 0
        piece = None            # Variable storing Square Object to be animated

        # Main game while loop
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

            
            #########################################     WHITE          #################################################################################################################
            
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

                            
                            if (clicked_row < ROWS and clicked_col < COLS and turn == "white" and dragger.piece.team == "white"):
                                if (result >= 1):                           # player drops piece into valid square

                                    if (self.game.board.whiteInCheck == False):
                                        capturedSquare = copy.deepcopy(game.board.grid[clicked_row][clicked_col])
                                        copygrid = copy.deepcopy(game.board.grid)
                                        saveinitial = copy.deepcopy(game.board.grid[dragger.initial_row][dragger.initial_col])
                                        copygrid[clicked_row][clicked_col] = saveinitial
                                        copygrid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                        if capturedSquare.team == "black":
                                            game.board.blackPieces.remove([clicked_row, clicked_col])
                                        game.board.loadProtections2(copygrid)
                                        inCheck = game.board.checkChecker("black", copygrid)

                                        if inCheck == False:    # boolean prevents moving a friendly piece towards opening a check towards white king

                                            if dragger.piece.piece == "pond" and clicked_row == 0:     # transform pond into Queen
                                                capturedSquare = copy.deepcopy(game.board.grid[clicked_row][clicked_col])
                                                game.board.grid[clicked_row][clicked_col] = Square(clicked_row, clicked_col)
                                                game.board.grid[clicked_row][clicked_col].add_piece("white", "queen", "images/whiteQueen.png", clicked_row, clicked_col)
                                                game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                if capturedSquare.team == "black":
                                                    game.board.blackPieces.remove([clicked_row, clicked_col])
                                                game.board.checkChecker("white", game.board.grid)
                                                turn = "black"

                                               

                                            else:
                                                # shift all piece information into new Square and Piece for capture
                                                game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                capturedSquare = copy.deepcopy(game.board.grid[clicked_row][clicked_col])
                                                game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                game.board.grid[clicked_row][clicked_col].moves = []
                                                game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                if capturedSquare.team == "black":
                                                    game.board.blackPieces.remove([clicked_row, clicked_col])
                                                turn = "black"
                                                if dragger.piece == 'king':
                                                    game.board.whiteKingLoc = [clicked_row, clicked_col]
                                                game.board.checkChecker("white", game.board.grid)
                                                        
                                    elif (self.game.board.whiteInCheck == True):
                                        # hypothetical checker

                                        copyBoard = copy.deepcopy(game.board)
                                        savepiece = game.board.grid[dragger.initial_row][dragger.initial_col]
                                        capturedSquare = copy.deepcopy(game.board.grid[clicked_row][clicked_col])
                                        copyBoard.grid[clicked_row][clicked_col] = savepiece
                                        copyBoard.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)

                                        if capturedSquare.team == "black":
                                            game.board.blackPieces.remove([clicked_row, clicked_col])

                                        copyBoard.checkChecker("black", copyBoard.grid)
                                        if copyBoard.whiteInCheck == False:
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

                            dragger.dragging = False
                            dragger.piece = None
                            dragger.object = None
                            game.board.loadProtections()
                            if game.board.blackInCheck == True:
                                game.board.InCheckMoves("black")

                            


                
        ################################################    BLACK        ##############################################################################################################


            elif turn == "black":

                

                if game.board.blackInCheck == False:
                    if thread1 == None and animating == False:
                        thread1 = threading.Thread(target=findMoveBlack, args=(game, q))
                        thread1.start()

                    if thread1.is_alive() == False and animating == False:
                        moves = q.get()
                        max_key = 0
                        for key in moves:
                            if key > max_key:
                                max_key = key
                        
                        print("max pts:", max_key)
                        index = int(len(moves[max_key]) / 2)
                        path = moves[max_key][index][0]
                        print("chosen path:", moves[max_key][index])

                        initial_row = path[0]
                        initial_col = path[1]
                        final_row = path[2]
                        final_col = path[3]

                        initial_x = copy.copy(initial_col) * 100
                        initial_y = copy.copy(initial_row) * 100
                        final_x = copy.copy(final_col) * 100
                        final_y = copy.copy(final_row) * 100

                        xIncrementer = copy.copy(initial_x)
                        yIncrementer = copy.copy(initial_y)

                        piece = copy.deepcopy(game.board.grid[initial_row][initial_col])
                        animating = True


                    if animating == True:
                        game.board.grid[initial_row][initial_col] = Square(initial_row, initial_col)
                        dx = (final_x - initial_x) / 10
                        dy = (final_y - initial_y) / 10
                        
                        if xIncrementer != final_x or yIncrementer != final_y:
                            img = pygame.image.load(piece.image)

                            original_width, original_height = img.get_size()

                            spacing_factor = 0.9

                            # Calculates scaling factors
                            width_scale = CELL_SIZE * spacing_factor / original_width
                            height_scale = CELL_SIZE * spacing_factor / original_height
                            # Use the smaller scaling factor to maintain aspect ratio
                            scale_factor = min(width_scale, height_scale)
                            # Scales the image
                            img = pygame.transform.scale(img, (int(original_width * scale_factor), int(original_height * scale_factor)))
                            img_center = (xIncrementer+50, yIncrementer+50)
                            screen.blit(img, img.get_rect(center=img_center))

                            xIncrementer += dx
                            yIncrementer += dy

                        elif xIncrementer == final_x and yIncrementer == final_y:
                            game.board.blackPieces.remove([initial_row, initial_col])    
                            game.board.blackPieces.append([final_row, final_col])                    
                            game.board.grid[initial_row][initial_col] = Square(initial_row, initial_col)

                            game.board.grid[final_row][final_col] = piece
                            game.board.grid[final_row][final_col].row = final_row
                            game.board.grid[final_row][final_col].col = final_col

                            if piece.piece == "king":
                                game.board.blackKingLoc = [final_row, final_col]

                            piece = None
                            thread1 = None
                            animating = False
                            game.board.loadProtections()
                            turn = "white"
                            game.board.checkChecker("black", game.board.grid)
                            if (game.board.whiteInCheck == True):
                                game.board.InCheckMoves("white")
                        
                


                elif game.board.blackInCheck == True:
                    print("BLACK IN CHECK")

                    blackmoves = game.board.black_move
                    if thread1 == None and animating == False:
                        thread1 = threading.Thread(target=findCheckMoveBlack, args=(game, blackmoves, q))
                        thread1.start()

                    if thread1.is_alive() == False and animating == False:
                        print("accessed once")
                        move = q.get()
                        if move != None:
                            initial_row = move[0]
                            initial_col = move[1]
                            final_row = move[2]
                            final_col = move[3]

                            initial_x = copy.copy(initial_col) * 100
                            initial_y = copy.copy(initial_row) * 100
                            final_x = copy.copy(final_col) * 100
                            final_y = copy.copy(final_row) * 100

                            xIncrementer = copy.copy(initial_x)
                            yIncrementer = copy.copy(initial_y)

                            piece = copy.deepcopy(game.board.grid[initial_row][initial_col])
                            animating = True

                        else:
                            # black is in checkmate
                            print("SPECIAL CASE ACCSESSED")
                            piece = None
                            thread1 = None
                            animating = False
                            game.board.blackInCheckmate == True
                            game.board.loadProtections()
                            turn = "white"

                    if animating == True:
                        print("ANIMATING")
                        game.board.grid[initial_row][initial_col] = Square(initial_row, initial_col)
                        dx = (final_x - initial_x) / 10
                        dy = (final_y - initial_y) / 10
                        
                        if xIncrementer != final_x or yIncrementer != final_y:
                            img = pygame.image.load(piece.image)

                            original_width, original_height = img.get_size()

                            spacing_factor = 0.9

                            # Calculates scaling factors
                            width_scale = CELL_SIZE * spacing_factor / original_width
                            height_scale = CELL_SIZE * spacing_factor / original_height
                            # Use the smaller scaling factor to maintain aspect ratio
                            scale_factor = min(width_scale, height_scale)
                            # Scales the image
                            img = pygame.transform.scale(img, (int(original_width * scale_factor), int(original_height * scale_factor)))
                            img_center = (xIncrementer+50, yIncrementer+50)
                            screen.blit(img, img.get_rect(center=img_center))

                            xIncrementer += dx
                            yIncrementer += dy

                        elif xIncrementer == final_x and yIncrementer == final_y:
                            print("PIECE DATA MOVED")
                            print("IS IT CHECKMATE?:", game.board.blackInCheckmate)
                            game.board.blackPieces.remove([initial_row, initial_col])    
                            game.board.blackPieces.append([final_row, final_col])                    
                            game.board.grid[initial_row][initial_col] = Square(initial_row, initial_col)

                            game.board.grid[final_row][final_col] = piece
                            game.board.grid[final_row][final_col].row = final_row
                            game.board.grid[final_row][final_col].col = final_col

                            if piece.piece == "king":
                                game.board.blackKingLoc = [final_row, final_col]

                            piece = None
                            thread1 = None
                            animating = False
                            game.board.blackInCheck == False
                            game.board.loadProtections()
                            turn = "white"
                            game.board.checkChecker("black", game.board.grid)
                            if (game.board.whiteInCheck == True):
                                game.board.InCheckMoves("white")


                


                
                    

                    
                    


            pygame.display.flip()
    
    


    

main = Main()
main.mainloop()
