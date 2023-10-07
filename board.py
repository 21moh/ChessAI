import pygame
import sys
import copy

from const import *
from piece import Piece
from square import Square


class Board:
    def __init__(self):
        self.grid = [[None for i in range(8)] for i in range(8)]    #square class, holds current piece and possible attacking pieces
        self.whiteKingLoc = [7, 4]
        self.blackKingLoc = [0, 4]

        self.blackInCheck = False
        self.blackBlocks = []
        self.blackKingMoves = []

        self.whiteInCheck = False
        self.whiteBlocks = []
        self.whiteKingMoves = []

        self.blackInCheckmate = False
        self.whiteInCheckmate = False


    def initialize_board(self):
        grid = self.grid
        for i in range(ROWS):
            for j in range(COLS):
                grid[i][j] = Square(i, j)
        
        
        for i in range(8):
            grid[1][i].add_piece("black", "pond", "images/blackPond.png", 1, i)
            grid[6][i].add_piece("white", "pond", "images/whitePond.png", 6, i)


        grid[0][0].add_piece("black", "rook", "images/blackRook.png", 0, 0)
        grid[0][7].add_piece("black", "rook", "images/blackRook.png", 0, 7)
        grid[7][0].add_piece("white", "rook", "images/whiteRook.png", 7, 0)
        grid[7][7].add_piece("white", "rook", "images/whiteRook.png", 7, 7)
        

        grid[0][1].add_piece("black", "knight", "images/blackKnight.png", 0, 1)
        grid[0][6].add_piece("black", "knight", "images/blackKnight.png", 0, 6)
        grid[7][1].add_piece("white", "knight", "images/whiteKnight.png", 7, 1)
        grid[7][6].add_piece("white", "knight", "images/whiteKnight.png", 7, 6)
        

        grid[0][2].add_piece("black", "bishop", "images/blackBishop.png", 0, 2)
        grid[0][5].add_piece("black", "bishop", "images/blackBishop.png", 0, 5)
        grid[7][2].add_piece("white", "bishop", "images/whiteBishop.png", 7, 2)
        grid[7][5].add_piece("white", "bishop", "images/whiteBishop.png", 7, 5)
        
        

        grid[0][3].add_piece("black", "queen", "images/blackQueen.png", 0, 3)
        grid[0][4].add_piece("black", "king", "images/blackKing.png", 0, 4)
        grid[7][3].add_piece("white", "queen", "images/whiteQueen.png", 7, 3)
        grid[7][4].add_piece("white", "king", "images/whiteKing.png", 7, 4)
        
        

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
                moves = self.get_moves(self.grid, grid[row][col].piece, row, col, grid[row][col].team)
                team = grid[row][col].team
                # since moves function includes moves for capturing, get rid of possible capture spots since that move is not a protection spot

                for loc in moves:
                    if grid[loc[0]][loc[1]].team == team or grid[loc[0]][loc[1]].piece == None:
                        if (team == "white"):
                            self.grid[loc[0]][loc[1]].whiteprotected = True
                        elif (team == "black"):
                            self.grid[loc[0]][loc[1]].blackprotected = True

    



    def loadPlacements(self, moves, turn, surface):

        grid = self.grid
            
        for i in range(len(moves)):
            if (grid[moves[i][0]][moves[i][1]].piece == None):  # No piece in location
                img = pygame.image.load("attack.png")

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

            elif (grid[moves[i][0]][moves[i][1]].team != None):
                if (turn != grid[moves[i][0]][moves[i][1]].team): # Enemy piece in location
                    img = pygame.image.load("cap_attack.png")

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
                    if (grid[row+2][col].piece == None):
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

                


        ##########################################
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

        
        ##########################################
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

        ##########################################
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



        ##########################################
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
                    if (grid[row-1][col].piece == None or (grid[row-1][col].team == "black" and grid[row][col].blackprotected == False)):
                        moves.append([row-1, col])
                    if (grid[row][col-1].piece == None or (grid[row][col-1].team == "black" and grid[row][col].blackprotected == False)):
                        moves.append([row, col-1])
                
                if (row < ROWS-1 and col < COLS-1):
                    if (grid[row+1][col+1].piece == None or (grid[row+1][col+1].team == "black" and grid[row+1][col+1].blackprotected == False)):
                        moves.append([row+1, col+1])
                    if (grid[row+1][col].piece == None or (grid[row+1][col].team == "black" and grid[row+1][col].blackprotected == False)):
                        moves.append([row+1, col])
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
                        moves.append([row-1, col-1])
                    if (grid[row-1][col].piece == None or (grid[row-1][col].team == "white" and grid[row-1][col].whiteprotected == False)):
                        moves.append([row-1, col])
                    if (grid[row][col-1].piece == None or (grid[row][col-1].team == "white" and grid[row][col-1].whiteprotected == False)):
                        moves.append([row, col-1])
                
                if (row < ROWS-1 and col < COLS-1):
                    if (grid[row+1][col+1].piece == None or (grid[row+1][col+1].team == "white" and grid[row+1][col+1].whiteprotected == False)):
                        moves.append([row+1, col+1])
                    if (grid[row+1][col].piece == None or (grid[row+1][col].team == "white" and grid[row+1][col].whiteprotected == False)):
                        moves.append([row+1, col])
                    if (grid[row][col+1].piece == None or (grid[row][col+1].team == "white" and grid[row][col+1].whiteprotected == False)):
                        moves.append([row, col+1])
                
                if (row > 0 and col < COLS-1):
                    if (grid[row-1][col+1].piece == None or (grid[row-1][col+1].team == "white" and grid[row-1][col+1].whiteprotected == False)):
                        moves.append([row-1, col+1])
                if (row < ROWS-1 and col > 0):
                    if (grid[row+1][col-1].piece == None or (grid[row+1][col-1].team == "white" and grid[row+1][col-1].whiteprotected == False)):
                        moves.append([row+1, col-1])
        
        return moves
    

    # need to write function that checks for pieces blocking checks
    
    

    def checkChecker(self, attacking_team):
        blackInCheckmate = True     # True until not true in function
        whiteInCheckmate = True     # True until not true in function

        if (attacking_team == "white"):
            
            kingloc = copy.deepcopy(self.blackKingLoc)
            attacking_pieces = []

            # check and get white attacking pieces towards the king
            for row in range(ROWS):
                for col in range(COLS):
                    if self.grid[row][col].team == "white":
                        if (self.get_moves(self.grid[row][col].piece, row, col, "white", self.grid).count(kingloc) >= 1 ): # if the piece on this square has a move that attacks the king location
                            attacking_pieces.append(self.grid[row][col])
            
            # if there are piece(s) attacking the white king --> check for available moves for white
            if (len(attacking_pieces) >= 1):
                self.blackInCheck = True
                # check for checkmate
                
                # check if there are any pieces that can block the checkmate
                for row in range(ROWS):
                    for col in range(COLS):
                        if self.grid[row][col].team == "black" and self.grid[row][col].piece != "king":
                            pieceMoves = self.get_moves(self.grid[row][col].piece, row, col, "black", self.grid)
                            for move in pieceMoves:
                                copygrid = copy.deepcopy(self.grid)
                                savePiece = copy.deepcopy(self.grid[row][col])
                                copygrid[move[0]][move[1]] = savePiece
                                copygrid[row][col] = Square(row, col)
                                result = []
                                for i in range(len(attacking_pieces)):
                                    if kingloc not in self.get_moves(attacking_pieces[i].piece, attacking_pieces[i].row, attacking_pieces[i].col, attacking_pieces[i].team, copygrid): # add grid part to function
                                        result.append(1)
                                if len(result) == len(attacking_pieces):
                                    blackInCheckmate = False
                                    self.blackBlocks.append([savePiece, move[0], move[1]])    # saves the exact piece and the place on the grid it can move as *Square object, row, col*
                
                # check if the king can move to avoid the checkmate
                kingMoves = self.get_moves(self.grid[kingloc[0]][kingloc[1]].piece, kingloc[0], kingloc[1], "black", self.grid)
                for moves in kingMoves:
                    copygrid = copy.deepcopy(self.grid)
                    initialpos = copy.deepcopy(copygrid[kingloc[0]][kingloc[1]])
                    copygrid[moves[0]][moves[1]] = initialpos
                    copygrid[kingloc[0]][kingloc[1]] = Square(initialpos.row, initialpos.col)
                    copykingloc = [moves[0], moves[1]]
                    result = []
                    for i in range(len(attacking_pieces)):
                        if copykingloc not in self.get_moves(attacking_pieces[i].piece, attacking_pieces[i].row, attacking_pieces[i].col, attacking_pieces[i].team, copygrid): # add grid part to function
                            result.append(1)
                    if len(result) == len(attacking_pieces):
                        blackInCheckmate = False
                        self.blackKingMoves.append(copykingloc)

                

                if (blackInCheckmate == True):        # black is in checkmate --> game over condition
                    self.blackInCheckmate = True
                    print("BLACK IN CHECKMATE GAME OVER")
            else:       # not in check
                pass

        elif (attacking_team == "black"):
            
            kingloc = copy.deepcopy(self.whiteKingLoc)
            attacking_pieces = []

            # check and get black attacking pieces towards the king
            for row in range(ROWS):
                for col in range(COLS):
                    if self.grid[row][col].team == "black":
                        if (self.get_moves(self.grid[row][col].piece, row, col, "black", self.grid).count(kingloc) >= 1 ): # if the piece on this square has a move that attacks the king location
                            attacking_pieces.append(self.grid[row][col])

            # if there are piece(s) attacking the white king --> check for available moves for white
            if (len(attacking_pieces) >= 1):
                self.whiteInCheck = True
                # check for checkmate
                
                # check if there are any pieces that can block the checkmate
                for row in range(ROWS):
                    for col in range(COLS):
                        if self.grid[row][col].team == "black" and self.grid[row][col].piece != "king":
                            pieceMoves = self.get_moves(self.grid[row][col].piece, row, col, "black", self.grid)
                            for move in pieceMoves:
                                copygrid = copy.deepcopy(self.grid)
                                savePiece = copy.deepcopy(self.grid[row][col])
                                copygrid[move[0]][move[1]] = savePiece
                                copygrid[row][col] = Square(row, col)
                                result = []
                                for i in range(len(attacking_pieces)):
                                    if kingloc not in self.get_moves(attacking_pieces[i].piece, attacking_pieces[i].row, attacking_pieces[i].col, attacking_pieces[i].team, copygrid): # add grid part to function
                                        result.append(1)
                                if len(result) == len(attacking_pieces):
                                    whiteInCheckmate = False
                                    self.whiteBlocks.append([savePiece, move[0], move[1]])    # saves the exact piece and the place on the grid it can move
                
                # check if the king can move to avoid the checkmate
                kingMoves = self.get_moves(self.grid[row][col].piece, row, col, "black", self.grid)
                for moves in kingMoves:
                    copygrid = copy.deepcopy(self.grid)
                    initialpos = copy.deepcopy(copygrid[kingloc[0]][kingloc[1]])
                    copygrid[moves[0]][moves[1]] = initialpos
                    copygrid[kingloc[0]][kingloc[1]] = Square(initialpos.row, initialpos.col)
                    copykingloc = [moves[0], moves[1]]
                    result = []
                    for i in range(len(attacking_pieces)):
                        if copykingloc not in self.get_moves(attacking_pieces[i].piece, attacking_pieces[i].row, attacking_pieces[i].col, attacking_pieces[i].team, copygrid): # add grid part to function
                            result.append(1)
                    if len(result) == len(attacking_pieces):
                        whiteInCheckmate = False
                        self.whiteKingMoves.append(copykingloc)

                

                if (whiteInCheckmate == True):        # black is in checkmate --> game over condition
                    self.whiteInCheckmate = True
                    print("WHITE IN CHECKMATE GAME OVER")
                
            
            
        
        
