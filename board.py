import pygame
import sys
import copy

from const import *
from square import Square


class Board:
    def __init__(self):
        self.grid = [[None for i in range(8)] for i in range(8)]    #square class, holds current piece and possible attacking pieces
        self.whiteKingLoc = [7, 4]
        self.blackKingLoc = [0, 4]

        self.blackInCheck = False
        self.black_move = []

        self.whiteInCheck = False
        self.whiteBlocks = []
        self.whiteKingMoves = []

        self.white_movable = []
        self.white_move = []

        self.blackInCheckmate = False
        self.whiteInCheckmate = False

        self.blackPieces = []


    def initialize_board(self):
        grid = self.grid
        blackpieces = self.blackPieces
        for i in range(ROWS):
            for j in range(COLS):
                grid[i][j] = Square(i, j)
        
        
        for i in range(8):
            grid[1][i].add_piece("black", "pond", "images/blackPond.png", 1, i)
            blackpieces.append([1, i])
            grid[6][i].add_piece("white", "pond", "images/whitePond.png", 6, i)
            grid[1][i].points = 1
            grid[6][i].points = 1


        grid[0][0].add_piece("black", "rook", "images/blackRook.png", 0, 0)
        grid[0][7].add_piece("black", "rook", "images/blackRook.png", 0, 7)
        blackpieces.append([0, 0])
        blackpieces.append([0, 7])
        grid[7][0].add_piece("white", "rook", "images/whiteRook.png", 7, 0)
        grid[7][7].add_piece("white", "rook", "images/whiteRook.png", 7, 7)
        grid[0][0].points = 5
        grid[0][7].points = 5
        grid[7][0].points = 5
        grid[7][7].points = 5
        

        grid[0][1].add_piece("black", "knight", "images/blackKnight.png", 0, 1)
        grid[0][6].add_piece("black", "knight", "images/blackKnight.png", 0, 6)
        blackpieces.append([0, 1])
        blackpieces.append([0, 6])
        grid[7][1].add_piece("white", "knight", "images/whiteKnight.png", 7, 1)
        grid[7][6].add_piece("white", "knight", "images/whiteKnight.png", 7, 6)
        grid[0][1].points = 3
        grid[0][6].points = 3
        grid[7][1].points = 3
        grid[7][6].points = 3
        

        grid[0][2].add_piece("black", "bishop", "images/blackBishop.png", 0, 2)
        grid[0][5].add_piece("black", "bishop", "images/blackBishop.png", 0, 5)
        blackpieces.append([0, 2])
        blackpieces.append([0, 5])
        grid[7][2].add_piece("white", "bishop", "images/whiteBishop.png", 7, 2)
        grid[7][5].add_piece("white", "bishop", "images/whiteBishop.png", 7, 5)
        grid[0][2].points = 3
        grid[0][5].points = 3
        grid[7][2].points = 3
        grid[7][5].points = 3
        
        

        grid[0][3].add_piece("black", "queen", "images/blackQueen.png", 0, 3)
        grid[0][4].add_piece("black", "king", "images/blackKing.png", 0, 4)
        blackpieces.append([0, 3])
        blackpieces.append([0, 4])
        grid[7][3].add_piece("white", "queen", "images/whiteQueen.png", 7, 3)
        grid[7][4].add_piece("white", "king", "images/whiteKing.png", 7, 4)
        grid[0][3].points = 10
        grid[0][4].points = 1000
        grid[7][3].points = 10
        grid[7][4].points = 1000

        """
        for row in range(ROWS):
            for col in range(COLS):
                grid[row][col].setPoint()
        """
        
        
    
    def loadPoints(self):
        grid = self.grid
        for row in range(ROWS):
            for col in range(COLS):
                grid[row][col].setPoint()
    
    def loadPlacements(self, moves, turn, surface):

        grid = self.grid
            
        for i in range(len(moves)):
            if (grid[moves[i][0]][moves[i][1]].piece == None):  # No piece in location
                img = pygame.image.load("images/attack2.png")

                original_width, original_height = img.get_size()

                spacing_factor = 0.6

                # Calculates scaling factors
                width_scale = CELL_SIZE * spacing_factor / original_width
                height_scale = CELL_SIZE * spacing_factor / original_height

                # Use the smaller scaling factor to maintain aspect ratio
                scale_factor = min(width_scale, height_scale)

                # Scales the image
                img = pygame.transform.scale(img, (int(original_width * scale_factor), int(original_height * scale_factor)))
                img_center = (moves[i][1] * CELL_SIZE+50, moves[i][0] * CELL_SIZE+50)

                surface.blit(img, img.get_rect(center=img_center))

            elif (grid[moves[i][0]][moves[i][1]].team != None):
                if (turn != grid[moves[i][0]][moves[i][1]].team): # Enemy piece in location
                    img = pygame.image.load("images/cap_attack2.png")

                    original_width, original_height = img.get_size()

                    spacing_factor = 0.8

                    # Calculates scaling factors
                    width_scale = CELL_SIZE * spacing_factor / original_width
                    height_scale = CELL_SIZE * spacing_factor / original_height

                    # Use the smaller scaling factor to maintain aspect ratio
                    scale_factor = min(width_scale, height_scale)

                    # Scales the image
                    img = pygame.transform.scale(img, (int(original_width * scale_factor), int(original_height * scale_factor)))
                    img_center = (moves[i][1] * CELL_SIZE+50, moves[i][0] * CELL_SIZE+50)

                    surface.blit(img, img.get_rect(center=img_center))

    def postAttackers(self):
        # loads each pieces' attackers on the board
        grid = self.grid
        for row in range(ROWS):
            for col in range(COLS):
                if grid[row][col].piece != None:
                    team = grid[row][col].team
                    moves = self.get_moves(grid[row][col].piece, row, col, team, self.grid)
                    for move in moves:
                        drow = move[0]
                        dcol = move[1]
                        if team == "white":
                            grid[drow][dcol].whiteAttackers.append([row, col])
                        elif team == "black":
                            grid[drow][dcol].whiteAttackers.append([row, col])

    def loadProtections(self):
        # loads all potential squares being attacked/protected on the board through self.whiteprotected and self.blackprotected in the square class
        grid = self.grid

        #refresh protections
        for row in range(ROWS):
            for col in range(COLS):
                self.grid[row][col].whiteprotected = False
                self.grid[row][col].blackprotected = False
        
        for row in range(ROWS):
            for col in range(COLS):
                moves = self.getProtections(grid[row][col].piece, row, col, grid[row][col].team, self.grid)
                team = grid[row][col].team
                # since moves function includes moves for capturing, get rid of possible capture spots since that move is not a protection spot

                for loc in moves:
                    if (team == "white"):
                        self.grid[loc[0]][loc[1]].whiteprotected = True
                    if (team == "black"):
                        self.grid[loc[0]][loc[1]].blackprotected = True

    
    def loadProtections2(self, grid):       # same as loadprotections but takes in grid argument (too much of my code used loadProtections)
        # loads all potential squares being attacked/protected on the board through self.whiteprotected and self.blackprotected in the square class

        #refresh protections
        for row in range(ROWS):
            for col in range(COLS):
                grid[row][col].whiteprotected = False
                grid[row][col].blackprotected = False
        
        for row in range(ROWS):
            for col in range(COLS):
                moves = self.getProtections(grid[row][col].piece, row, col, grid[row][col].team, grid)
                team = grid[row][col].team
                # since moves function includes moves for capturing, get rid of possible capture spots since that move is not a protection spot

                for loc in moves:
                    if (team == "white"):
                        grid[loc[0]][loc[1]].whiteprotected = True
                    if (team == "black"):
                        grid[loc[0]][loc[1]].blackprotected = True
        
    




    def printProtections(self): # debugging purposes
        num = 0
        for row in range(ROWS):
            for col in range(COLS):
                if (self.grid[row][col].whiteprotected == True and self.grid[row][col].blackprotected == True):
                    print("WB ", end="")
                elif self.grid[row][col].whiteprotected == True:
                    print("W  ", end="")
                elif self.grid[row][col].blackprotected == True:
                    print("B  ",end="")
                else:
                    print(".  ",end="")
                num = num + 1
            print()

        print()
        print()

    def printProtections2(self, grid): # debugging purposes
        print("FOR COPYGRID")
        num = 0
        for row in range(ROWS):
            for col in range(COLS):
                if (grid[row][col].whiteprotected == True and grid[row][col].blackprotected == True):
                    print("WB ", end="")
                elif grid[row][col].whiteprotected == True:
                    print("W  ", end="")
                elif grid[row][col].blackprotected == True:
                    print("B  ",end="")
                else:
                    print(".  ",end="")
                num = num + 1
            print()

        print()
        

    def checkChecker(self, defending_team, grid):

        if (defending_team == "black"):     # for black
            kingloc = copy.deepcopy(self.blackKingLoc)
            attacking_pieces = []
            for row in range(ROWS):
                for col in range(COLS):
                    if grid[row][col].team == "white":
                        if (self.get_moves(grid[row][col].piece, row, col, "white", grid).count(kingloc) >= 1 ): # if the piece on this square has a move that attacks the king location
                            attacking_pieces.append(grid[row][col])
            if (len(attacking_pieces) >= 1):
                self.blackInCheck = True
                return True
            else:
                self.blackInCheck = False
                return False
        
        elif (defending_team == "white"):       # for white
            kingloc = copy.deepcopy(self.whiteKingLoc)
            attacking_pieces = []
            for row in range(ROWS):
                for col in range(COLS):
                    if grid[row][col].team == "black":
                        if (self.get_moves(grid[row][col].piece, row, col, "black", grid).count(kingloc) >= 1 ): # if the piece on this square has a move that attacks the king location
                            attacking_pieces.append(grid[row][col])
            if (len(attacking_pieces) >= 1):
                self.whiteInCheck = True
                return True
            else:
                self.whiteInCheck = False
                return False
            

    def InCheckMoves(self, defending_team):         # only needed for black recursion function
        
        if (defending_team == "white"):
            self.white_movable = [] # holds Square Object
            self.white_move = []   # holds corresponding move as a list --> index of move matches index of movable_pieces
            if self.whiteInCheck == True:
                for row in range(ROWS):
                    for col in range(COLS):
                        if self.grid[row][col].team == "white":
                            piece_moves = self.get_moves(self.grid[row][col].piece, row, col, "white", self.grid)
                            piece = self.grid[row][col].piece
                            for move in piece_moves:
                                copygrid = copy.deepcopy(self.grid)
                                copykingloc = copy.deepcopy(self.whiteKingLoc)
                                self.loadProtections2(copygrid)
                                save_initial = copy.deepcopy(copygrid[row][col])
                                copygrid[move[0]][move[1]] = save_initial
                                copygrid[row][col] = Square(row, col)
                                copygrid[move[0]][move[1]].row = move[0]
                                copygrid[move[0]][move[1]].col = move[1]
                                self.loadProtections2(copygrid)
                                if piece == "king":
                                    copykingloc = [move[0], move[1]]
                                if copygrid[copykingloc[0]][copykingloc[1]].blackprotected == False:
                                    self.white_movable.append(save_initial)
                                    self.white_move.append([move[0], move[1]])

            
            if len(self.white_movable) == 0:
                self.whiteInCheckmate = True


        elif (defending_team == "black"):
            #self.black_movable = [] # holds Square Object
            self.black_move = []   # holds corresponding move as a list --> index of move matches index of movable_pieces
            if self.blackInCheck == True:
                for row in range(ROWS):
                    for col in range(COLS):
                        if self.grid[row][col].team == "black":
                            piece_moves = self.get_moves(self.grid[row][col].piece, row, col, "black", self.grid)
                            irow = row
                            icol = col
                            for move in piece_moves:
                                frow = move[0]
                                fcol = move[1]
                                copygrid = copy.deepcopy(self.grid)
                                copyPiece = copy.deepcopy(self.grid[irow][icol])
                                copygrid[irow][icol] = Square(irow, icol)
                                copygrid[frow][fcol] = copyPiece
                                if copyPiece.piece == "king":
                                    pass
            
            #if len(self.black_movable) == 0:
            #    self.blackInCheckmate = True

    def CanCastle(self, team):
        if (team == "white"):
            directions = []
            if self.whiteKingLoc == [7,4] and self.grid[7][7].piece == "rook" and self.whiteInCheck == False:
                copygrid = copy.deepcopy(self.grid)
                if copygrid[7][5].piece == None and copygrid[7][6].piece == None:
                    saveKing = copy.deepcopy(copygrid[7][4])
                    copygrid[7][6] = saveKing
                    copygrid[7][4] = Square(7, 4)
                    saveRook = copy.deepcopy(copygrid[7][7])
                    copygrid[7][5] = saveRook
                    copygrid[7][7] = Square(7,7)
                    self.loadProtections2(copygrid)
                    if copygrid[7][6].blackprotected == False:
                        directions.append("right")
                
            if self.whiteKingLoc == [7,4] and self.grid[7][0].piece == "rook" and self.whiteInCheck == False:
                copygrid = copy.deepcopy(self.grid)
                if copygrid[7][1].piece == None and copygrid[7][2].piece == None and copygrid[7][3].piece == None:
                    saveKing = copy.deepcopy(copygrid[7][4])
                    copygrid[7][6] = saveKing
                    copygrid[7][4] = Square(7, 4)
                    saveRook = copy.deepcopy(copygrid[7][0])
                    copygrid[7][5] = saveRook 
                    copygrid[7][7] = Square(7,0)
                    self.loadProtections2(copygrid)
                    if copygrid[7][2].blackprotected == False:
                        directions.append("left")

            return directions

        if (team == "black"):
            directions = []
            if self.blackKingLoc == [0,4] and self.grid[0][7].piece == "rook" and self.blackInCheck == False:
                copygrid = copy.deepcopy(self.grid)
                if copygrid[0][5].piece == None and copygrid[7][6].piece == None:
                    saveKing = copy.deepcopy(copygrid[0][4])
                    copygrid[0][6] = saveKing
                    copygrid[0][4] = Square(0, 4)
                    saveRook = copy.deepcopy(copygrid[0][7])
                    copygrid[0][5] = saveRook
                    copygrid[0][7] = Square(0,7)
                    self.loadProtections2(copygrid)
                    if copygrid[0][6].whiteprotected == False:
                        directions.append("right")
                
            if self.blackKingLoc == [0,4] and self.grid[0][0].piece == "rook" and self.blackInCheck == False:
                copygrid = copy.deepcopy(self.grid)
                if copygrid[0][1].piece == None and copygrid[0][2].piece == None and copygrid[0][3].piece == None:
                    saveKing = copy.deepcopy(copygrid[0][4])
                    copygrid[0][6] = saveKing
                    copygrid[0][6] = Square(0, 5)
                    saveRook = copy.deepcopy(copygrid[0][0])
                    copygrid[0][4] = saveRook
                    copygrid[0][0] = Square(0,0)
                    self.loadProtections2(copygrid)
                    if copygrid[0][2].whiteprotected == False:
                        directions.append("left")
            
            return directions
            

            

    def Castle(self, team, direction):
        grid = self.grid
        if (team == "white"):
            if direction == "right":
                saveKing = copy.deepcopy(grid[7][4])
                grid[7][6] = saveKing
                grid[7][4] = Square(7, 4)
                saveRook = copy.deepcopy(grid[7][7])
                grid[7][5] = saveRook
                grid[7][7] = Square(7,7)
                self.whiteKingLoc = [7, 6]
                    
            if direction == "left":
                saveKing = copy.deepcopy(grid[7][4])
                grid[7][2] = saveKing
                grid[7][4] = Square(7, 4)
                saveRook = copy.deepcopy(grid[7][0])
                grid[7][5] = saveRook
                grid[7][7] = Square(7,0)
                self.whiteKingLoc = [7, 2]

        if (team == "black"):
            if direction == "right":
                saveKing = copy.deepcopy(grid[0][4])
                grid[0][6] = saveKing
                grid[0][4] = Square(0, 4)
                saveRook = copy.deepcopy(grid[0][7])
                grid[0][5] = saveRook
                grid[0][7] = Square(0,7)
                self.whiteKingLoc = [7, 6]
                    
            if direction == "left":
                saveKing = copy.deepcopy(grid[0][4])
                grid[0][2] = saveKing
                grid[0][4] = Square(0, 4)
                saveRook = copy.deepcopy(grid[0][0])
                grid[0][5] = saveRook
                grid[0][7] = Square(0,0)
                self.whiteKingLoc = [0, 2]

            
                
    

    def getProtections(self, piece, row, col, team, grid):
        self.row = row
        self.col = col
        self.team = team
        moves = []

        if (piece == "pond"):
            if (self.team == "white"):
                
                if (row == 6):
                    if (col >= 0 and col < 7):
                        if (grid[row-1][col+1].team == "white" or grid[row-1][col+1].piece == None or grid[row-1][col+1].team == "black"):
                            moves.append([row-1, col+1])
                    if (col > 0 and col <= COLS - 1):
                        if (grid[row-1][col-1].team == "white" or grid[row-1][col-1].piece == None or grid[row-1][col-1].team == "black"):
                            moves.append([row-1, col-1])
                    
                if (row >= 1 and row <= 5):

                    if (col >= 0 and col < COLS - 1):
                        if (grid[row-1][col+1].team == "white" or grid[row-1][col+1].piece == None or grid[row-1][col+1].team == "black"):
                            moves.append([row-1, col+1])
                    if (col > 0 and col <= COLS - 1):
                        if (grid[row-1][col-1].team == "white" or grid[row-1][col-1].piece == None or grid[row-1][col-1].team == "black"):
                            moves.append([row-1, col-1])

               

            elif (self.team == "black"):
                
                if (row == 1):
                    if (col >= 0 and col < COLS - 1):
                        if (grid[row+1][col+1].team != None or grid[row+1][col+1].piece == None):
                            moves.append([row+1, col+1])
                    if (col > 0 and col <= COLS - 1):
                        if (grid[row+1][col-1].team != None or grid[row+1][col-1].piece == None):
                            moves.append([row+1, col-1])
                    
                if (row >= 2 and row <= 6):
                    if (col >= 0 and col < COLS - 1):
                        if (grid[row+1][col+1].team != None or grid[row+1][col+1].piece == None):
                            moves.append([row+1, col+1])
                    if (col > 0 and col <= COLS - 1):
                        if (grid[row+1][col-1].team != None or grid[row+1][col-1].piece == None):
                            moves.append([row+1, col-1])

                


        ##########################################
        elif (piece == "bishop"):

            copy_row = self.row
            copy_col = self.col

            
            
            if (team == "white"):

                while (row >= 0 and col >= 0):
                    row = row - 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].piece != None):
                        moves.append([row, col])

                    if (grid[row][col].piece != None or grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col
                while (row >= 0 and col < COLS-1):
                    row = row - 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                    
                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col >= 0):
                    row = row + 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col < COLS-1):
                    row = row + 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break

            elif(self.team == "black"):

                while (row > 0 and col > 0):
                    row = row - 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])

                    if (grid[row][col].piece != None or grid[row][col].team != None):
                        break

                row = copy_row
                col = copy_col
                while (row > 0 and col < COLS-1):
                    row = row - 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                    
                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col > 0):
                    row = row + 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col < COLS-1):
                    row = row + 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break

        
        ##########################################
        elif (piece == "knight"):

            

            if (self.team == "white"):
                if (row-2 >= 0 and col-1 >= 0):
                    if (grid[row-2][col-1].piece == None or grid[row-2][col-1].team != None):
                        moves.append([row-2, col-1])
                if (row-2 >= 0 and col+1 <= COLS-1):
                    if (grid[row-2][col+1].piece == None or grid[row-2][col+1].team != None):
                        moves.append([row-2, col+1])
                if (row-1 >= 0 and col-2 >= 0):
                    if (grid[row-1][col-2].piece == None or grid[row-1][col-2].team != None):
                        moves.append([row-1, col-2])
                if (row+1 <= ROWS-1 and col-2 >= 0):
                    if (grid[row+1][col-2].piece == None or grid[row+1][col-2].team != None):
                        moves.append([row+1, col-2])
                if (row+2 <= ROWS-1 and col-1 >= 0):
                    if (grid[row+2][col-1].piece == None or grid[row+2][col-1].team != None):
                        moves.append([row+2, col-1])
                if (row+2 <= ROWS-1 and col+1 <= COLS-1):
                    if (grid[row+2][col+1].piece == None or grid[row+2][col+1].team != None):
                        moves.append([row+2, col+1])
                if (row+1 <= ROWS-1 and col+2 <= COLS-1):
                    if (grid[row+1][col+2].piece == None or grid[row+1][col+2].team != None):
                        moves.append([row+1, col+2])
                if (row-1 >=0 and col+2 <= COLS-1):
                    if (grid[row-1][col+2].piece == None or grid[row-1][col+2].team != None):
                        moves.append([row-1, col+2])


            elif (self.team == "black"):
                if (row-2 >= 0 and col-1 >= 0):
                    if (grid[row-2][col-1].piece == None or grid[row-2][col-1].team != None):
                        moves.append([row-2, col-1])
                if (row-2 >= 0 and col+1 <= COLS-1):
                    if (grid[row-2][col+1].piece == None or grid[row-2][col+1].team != None):
                        moves.append([row-2, col+1])
                if (row-1 >= 0 and col-2 >= 0):
                    if (grid[row-1][col-2].piece == None or grid[row-1][col-2].team != None):
                        moves.append([row-1, col-2])
                if (row+1 <= ROWS-1 and col-2 >= 0):
                    if (grid[row+1][col-2].piece == None or grid[row+1][col-2].team != None):
                        moves.append([row+1, col-2])
                if (row+2 <= ROWS-1 and col-1 >= 0):
                    if (grid[row+2][col-1].piece == None or grid[row+2][col-1].team != None):
                        moves.append([row+2, col-1])
                if (row+2 <= ROWS-1 and col+1 <= COLS-1):
                    if (grid[row+2][col+1].piece == None or grid[row+2][col+1].team != None):
                        moves.append([row+2, col+1])
                if (row+1 <= ROWS-1 and col+2 <= COLS-1):
                    if (grid[row+1][col+2].piece == None or grid[row+1][col+2].team != None):
                        moves.append([row+1, col+2])
                if (row-1 >=0 and col+2 <= COLS-1):
                    if (grid[row-1][col+2].piece == None or grid[row-1][col+2].team != None):
                        moves.append([row-1, col+2])

        ##########################################
        elif (piece == "rook"):
            copy_row = self.row
            copy_col = self.col

            if team == "white":

                while (row > 0):
                    row = row - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].team != None):
                        break
                row = copy_row

                while (row < ROWS-1):
                    row = row + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].team != None):
                        break
                row = copy_row

                while (col > 0):
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].team != None):
                        break
                col = copy_col
                
                while (col < COLS-1):
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].team != None):
                        break

            elif team == "black":

                while (row > 0):
                    row = row - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].team != None):
                        break
                row = copy_row

                while (row < ROWS-1):
                    row = row + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].team != None):
                        break
                row = copy_row

                while (col > 0):
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].team != None):
                        break
                col = copy_col
                
                while (col < COLS-1):
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].team != None):
                        break



        ##########################################
        elif (piece == "queen"):
            copy_row = self.row
            copy_col = self.col
            if (team == "white"):

                ### diagonal moves
                while (row > 0 and col > 0):
                    row = row - 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])

                    if (grid[row][col].piece != None or grid[row][col].team != None):
                        break

                row = copy_row
                col = copy_col
                while (row > 0 and col < COLS-1):
                    row = row - 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                    
                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col > 0):
                    row = row + 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col < COLS-1):
                    row = row + 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col

                ### horizontal moves
                while (row > 0):
                    row = row - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                row = copy_row

                while (row < ROWS-1):
                    row = row + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                row = copy_row

                while (col > 0):
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                col = copy_col
                
                while (col < COLS-1):
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                col = copy_col
            
            elif (team == "black"):
                
                while (row > 0 and col > 0):
                    row = row - 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])

                    if (grid[row][col].piece != None or grid[row][col].team != None):
                        break

                row = copy_row
                col = copy_col
                while (row > 0 and col < COLS-1):
                    row = row - 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                    
                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col > 0):
                    row = row + 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col < COLS-1):
                    row = row + 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col

                while (row > 0):
                    row = row - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                row = copy_row

                while (row < ROWS-1):
                    row = row + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                row = copy_row

                while (col > 0):
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                col = copy_col
                
                while (col < COLS-1):
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team != None):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                col = copy_col

        ##########################################
        elif (piece == "king"):
            if team == "white":
                if (row > 0 and col > 0):
                    if (grid[row-1][col-1].team == "white" or grid[row-1][col-1].blackprotected == False):
                        moves.append([row-1, col-1])
                if (row > 0):
                    if (grid[row-1][col].team == "white" or grid[row-1][col].blackprotected == False):
                        moves.append([row-1, col])
                    
                if (col > 0):
                    if (grid[row][col-1].team == "white" or grid[row][col-1].blackprotected == False):
                        moves.append([row, col-1])

                if (row < ROWS-1 and col < COLS-1):
                    if (grid[row+1][col+1].team == "white" or grid[row+1][col+1].blackprotected == False):
                        moves.append([row+1, col+1])
                
                if (row < ROWS-1):
                    if (grid[row-1][col].team == "white" or grid[row-1][col].blackprotected == False):
                        moves.append([row+1, col])
                    
                if (col < COLS-1):
                    if (grid[row][col+1].team == "white" or grid[row][col+1].blackprotected == False):
                        moves.append([row, col+1])

                if (row > 0 and col < COLS-1):
                    if (grid[row-1][col+1].team == "white" or grid[row-1][col+1].blackprotected == False):
                        moves.append([row-1, col+1])

                if (row < ROWS-1 and col > 0):
                    if (grid[row+1][col-1].team == "white" or grid[row+1][col-1].blackprotected == False):
                        moves.append([row+1, col-1])
                
            
            elif team == "black":
                if (row > 0 and col > 0):
                    if (grid[row-1][col-1].team == "black" or grid[row-1][col-1].whiteprotected == False):
                        moves.append([row-1, col-1])
                if (row > 0):
                    if (grid[row-1][col].team == "black" or grid[row-1][col].whiteprotected == False):
                        moves.append([row-1, col])
                    
                if (col > 0):
                    if (grid[row][col-1].team == "black" or grid[row][col-1].whiteprotected == False):
                        moves.append([row, col-1])

                if (row < ROWS-1 and col < COLS-1):
                    if (grid[row+1][col+1].team == "black" or grid[row+1][col+1].whiteprotected == False):
                        moves.append([row+1, col+1])
                
                if (row < ROWS-1):
                    if (grid[row-1][col].team == "black" or grid[row-1][col].whiteprotected == False):
                        moves.append([row-1, col])
                    
                if (col < COLS-1):
                    if (grid[row][col-1].team == "black" or grid[row][col-1].whiteprotected == False):
                        moves.append([row, col-1])

                if (row > 0 and col < COLS-1):
                    if (grid[row-1][col+1].team == "black" or grid[row-1][col+1].whiteprotected == False):
                        moves.append([row-1, col+1])

                if (row < ROWS-1 and col > 0):
                    if (grid[row+1][col-1].team == "black" or grid[row+1][col-1].whiteprotected == False):
                        moves.append([row+1, col-1])
        
        return moves




######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################



    def get_moves(self, piece, row, col, team, grid):
        self.row = row
        self.col = col
        self.team = team
        moves = []

        if (piece == "pond"):
            if (self.team == "white"):
                
                if (row == 6):
                    if (grid[row-1][col].piece == None):
                        moves.append([row-1, col])
                    if (grid[row-2][col].piece == None and grid[row-1][col].piece == None):
                        moves.append([row-2, col])
                    if (col >= 0 and col < COLS - 1):
                        if (grid[row-1][col+1].team == "black"):
                            moves.append([row-1, col+1])
                    if (col > 0 and col <= COLS - 1):
                        if (grid[row-1][col-1].team == "black"):
                            moves.append([row-1, col-1])
                    
                if (row >= 1 and row <= 5):
                    if (grid[row-1][col].piece == None):
                        moves.append([row-1, col])
                    if (col >= 0 and col < COLS - 1):
                        if (grid[row-1][col+1].team == "black"):
                            moves.append([row-1, col+1])
                    if (col > 0 and col <= COLS - 1):
                        if (grid[row-1][col-1].team == "black"):
                            moves.append([row-1, col-1])    

            elif (self.team == "black"):
                
                if (row == 1):
                    if (grid[row+1][col].piece == None):
                        moves.append([row+1, col])
                    if (grid[row+2][col].piece == None and grid[row+1][col].piece == None):
                        moves.append([row+2, col])
                    if (col >= 0 and col < COLS - 1):
                        if (grid[row+1][col+1].team == "white"):
                            moves.append([row+1, col+1])
                    if (col > 0 and col <= COLS - 1):
                        if (grid[row+1][col-1].team == "white"):
                            moves.append([row+1, col-1])
                    
                if (row >= 2 and row <= 6):
                    if (grid[row+1][col].piece == None):
                        moves.append([row+1, col])
                    if (col >= 0 and col < COLS - 1):
                        if (grid[row+1][col+1].team == "white"):
                            moves.append([row+1, col+1])
                    if (col > 0 and col <= COLS - 1):
                        if (grid[row+1][col-1].team == "white"):
                            moves.append([row+1, col-1])

        elif (piece == "bishop"):

            copy_row = self.row
            copy_col = self.col
            if (team == "white"):

                while (row > 0 and col > 0):
                    row = row - 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])

                    if (grid[row][col].piece != None or grid[row][col].team == "black"):
                        break

                row = copy_row
                col = copy_col
                while (row > 0 and col < COLS-1):
                    row = row - 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None or grid[row][col].team == "black"):
                        break
                    
                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col > 0):
                    row = row + 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None or grid[row][col].team == "black"):
                        break

                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col < COLS-1):
                    row = row + 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None or grid[row][col].team == "black"):
                        break

            elif(self.team == "black"):

                while (row > 0 and col > 0):
                    row = row - 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])

                    if (grid[row][col].piece != None or grid[row][col].team == "white"):
                        break

                row = copy_row
                col = copy_col
                while (row > 0 and col < COLS-1):
                    row = row - 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None or grid[row][col].team == "white"):
                        break
                    
                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col > 0):
                    row = row + 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None or grid[row][col].team == "white"):
                        break

                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col < COLS-1):
                    row = row + 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None or grid[row][col].team == "white"):
                        break
        
        elif (piece == "knight"):

            if (self.team == "white"):
                if (row-2 >= 0 and col-1 >= 0):
                    if (grid[row-2][col-1].piece == None or grid[row-2][col-1].team == "black"):
                        moves.append([row-2, col-1])
                if (row-2 >= 0 and col+1 <= COLS-1):
                    if (grid[row-2][col+1].piece == None or grid[row-2][col+1].team == "black"):
                        moves.append([row-2, col+1])
                if (row-1 >= 0 and col-2 >= 0):
                    if (grid[row-1][col-2].piece == None or grid[row-1][col-2].team == "black"):
                        moves.append([row-1, col-2])
                if (row+1 <= ROWS-1 and col-2 >= 0):
                    if (grid[row+1][col-2].piece == None or grid[row+1][col-2].team == "black"):
                        moves.append([row+1, col-2])
                if (row+2 <= ROWS-1 and col-1 >= 0):
                    if (grid[row+2][col-1].piece == None or grid[row+2][col-1].team == "black"):
                        moves.append([row+2, col-1])
                if (row+2 <= ROWS-1 and col+1 <= COLS-1):
                    if (grid[row+2][col+1].piece == None or grid[row+2][col+1].team == "black"):
                        moves.append([row+2, col+1])
                if (row+1 <= ROWS-1 and col+2 <= COLS-1):
                    if (grid[row+1][col+2].piece == None or grid[row+1][col+2].team == "black"):
                        moves.append([row+1, col+2])
                if (row-1 >=0 and col+2 <= COLS-1):
                    if (grid[row-1][col+2].piece == None or grid[row-1][col+2].team == "black"):
                        moves.append([row-1, col+2])


            elif (self.team == "black"):
                if (row-2 >= 0 and col-1 >= 0):
                    if (grid[row-2][col-1].piece == None or grid[row-2][col-1].team == "white"):
                        moves.append([row-2, col-1])
                if (row-2 >= 0 and col+1 <= COLS-1):
                    if (grid[row-2][col+1].piece == None or grid[row-2][col+1].team == "white"):
                        moves.append([row-2, col+1])
                if (row-1 >= 0 and col-2 >= 0):
                    if (grid[row-1][col-2].piece == None or grid[row-1][col-2].team == "white"):
                        moves.append([row-1, col-2])
                if (row+1 <= ROWS-1 and col-2 >= 0):
                    if (grid[row+1][col-2].piece == None or grid[row+1][col-2].team == "white"):
                        moves.append([row+1, col-2])
                if (row+2 <= ROWS-1 and col-1 >= 0):
                    if (grid[row+2][col-1].piece == None or grid[row+2][col-1].team == "white"):
                        moves.append([row+2, col-1])
                if (row+2 <= ROWS-1 and col+1 <= COLS-1):
                    if (grid[row+2][col+1].piece == None or grid[row+2][col+1].team == "white"):
                        moves.append([row+2, col+1])
                if (row+1 <= ROWS-1 and col+2 <= COLS-1):
                    if (grid[row+1][col+2].piece == None or grid[row+1][col+2].team == "white"):
                        moves.append([row+1, col+2])
                if (row-1 >=0 and col+2 <= COLS-1):
                    if (grid[row-1][col+2].piece == None or grid[row-1][col+2].team == "white"):
                        moves.append([row-1, col+2])

        elif (piece == "rook"):
            copy_row = self.row
            copy_col = self.col

            if team == "white":

                while (row > 0):
                    row = row - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                row = copy_row

                while (row < ROWS-1):
                    row = row + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                row = copy_row

                while (col > 0):
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                col = copy_col
                
                while (col < COLS-1):
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break

            elif team == "black":

                while (row > 0):
                    row = row - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                row = copy_row

                while (row < ROWS-1):
                    row = row + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                row = copy_row

                while (col > 0):
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                col = copy_col
                
                while (col < COLS-1):
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
        
        elif (piece == "queen"):
            copy_row = self.row
            copy_col = self.col
            if (team == "white"):

                ### diagonal moves
                while (row > 0 and col > 0):
                    row = row - 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])

                    if (grid[row][col].piece != None or grid[row][col].team == "black"):
                        break

                row = copy_row
                col = copy_col
                while (row > 0 and col < COLS-1):
                    row = row - 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                    
                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col > 0):
                    row = row + 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col < COLS-1):
                    row = row + 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col

                ### horizontal moves
                while (row > 0):
                    row = row - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                row = copy_row

                while (row < ROWS-1):
                    row = row + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                row = copy_row

                while (col > 0):
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                col = copy_col
                
                while (col < COLS-1):
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                col = copy_col
            
            elif (team == "black"):
                
                while (row > 0 and col > 0):
                    row = row - 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])

                    if (grid[row][col].piece != None or grid[row][col].team == "white"):
                        break

                row = copy_row
                col = copy_col
                while (row > 0 and col < COLS-1):
                    row = row - 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                    
                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col > 0):
                    row = row + 1
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col < COLS-1):
                    row = row + 1
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col

                while (row > 0):
                    row = row - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                row = copy_row

                while (row < ROWS-1):
                    row = row + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                row = copy_row

                while (col > 0):
                    col = col - 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                col = copy_col
                
                while (col < COLS-1):
                    col = col + 1
                    if (grid[row][col].piece == None or grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (grid[row][col].piece != None):
                        break
                col = copy_col

        ##########################################
        elif (piece == "king"):
            if team == "white":
                if (row > 0 and col > 0):
                    if (grid[row-1][col-1].piece == None or (grid[row-1][col-1].team == "black" and grid[row-1][col-1].blackprotected == False)):
                        moves.append([row-1, col-1])
                if row > 0:   
                    if (grid[row-1][col].piece == None or (grid[row-1][col].team == "black" and grid[row-1][col].blackprotected == False)):
                        moves.append([row-1, col])
                    
                if row >= 0 and col >= 1:
                    if (grid[row][col-1].piece == None or (grid[row][col-1].team == "black" and grid[row][col-1].blackprotected == False)):
                        moves.append([row, col-1])
                
                if (row < ROWS-1 and col < COLS-1):
                    if (grid[row+1][col+1].piece == None or (grid[row+1][col+1].team == "black" and grid[row+1][col+1].blackprotected == False)):
                        moves.append([row+1, col+1])
                    if (grid[row+1][col].piece == None or (grid[row+1][col].team == "black" and grid[row+1][col].blackprotected == False)):
                        moves.append([row+1, col])
                
                if row <= ROWS-1 and col < COLS-1:  
                    if (grid[row][col+1].piece == None or (grid[row][col+1].team == "black" and grid[row][col+1].blackprotected == False)):
                        moves.append([row, col+1])
                
                if (row > 0 and col < COLS-1):
                    if (grid[row-1][col+1].piece == None or (grid[row-1][col+1].team == "black" and grid[row-1][col+1].blackprotected == False)):
                        moves.append([row-1, col+1])
                if (row < ROWS-1 and col > 0):
                    if (grid[row+1][col-1].piece == None or (grid[row+1][col-1].team == "black" and grid[row+1][col-1].blackprotected == False)):
                        moves.append([row+1, col-1])
            
            elif team == "black":
                if (row > 0 and col > 0):
                    if (grid[row-1][col-1].piece == None or (grid[row-1][col-1].team == "white" and grid[row-1][col-1].whiteprotected == False)):
                        moves.append([row-1, col-1]) # <^
                    if (grid[row-1][col].piece == None or (grid[row-1][col].team == "white" and grid[row-1][col].whiteprotected == False)):
                        moves.append([row-1, col]) # ^
                
                if row >= 0 and col >= 1:
                    if (grid[row][col-1].piece == None or (grid[row][col-1].team == "white" and grid[row][col-1].whiteprotected == False)):
                        moves.append([row, col-1])  # <
                
                if (row < ROWS-1 and col < COLS-1):
                    if (grid[row+1][col+1].piece == None or (grid[row+1][col+1].team == "white" and grid[row+1][col+1].whiteprotected == False)):
                        moves.append([row+1, col+1])    #  down >
                    if (grid[row+1][col].piece == None or (grid[row+1][col].team == "white" and grid[row+1][col].whiteprotected == False)):
                        moves.append([row+1, col])  # down 
                
                if row <= ROWS-1 and col < COLS-1:  
                    if (grid[row][col+1].piece == None or (grid[row][col+1].team == "white" and grid[row][col+1].whiteprotected == False)):
                        moves.append([row, col+1])  # move to the right
                
                if (row > 0 and col < COLS-1):
                    if (grid[row-1][col+1].piece == None or (grid[row-1][col+1].team == "white" and grid[row-1][col+1].whiteprotected == False)):
                        moves.append([row-1, col+1])
                if (row < ROWS-1 and col > 0):
                    if (grid[row+1][col-1].piece == None or (grid[row+1][col-1].team == "white" and grid[row+1][col-1].whiteprotected == False)):
                        moves.append([row+1, col-1])
        
        return moves
    
                
                
            
            
        
        
