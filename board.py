import pygame
import sys

from const import *
from piece import Piece
from square import Square

class Board:
    def __init__(self):
        self.grid = [[None for i in range(8)] for i in range(8)]    #square class, holds current piece and possible attacking pieces
        self.white_locs = {}
        self.black_locs = {}
        self.whiteCheck = False
        self.blackCheck = False
        self.attackingWhiteforCheck = []
        self.attackingBlackforCheck = []

    def initialize_board(self):
        white_locs = self.white_locs
        black_locs = self.black_locs
        grid = self.grid
        for i in range(ROWS):
            for j in range(COLS):
                grid[i][j] = Square(i, j)
        
        white_locs["pond"] = []
        black_locs["pond"] = []
        white_locs["knight"] = []
        black_locs["knight"] = []
        white_locs["bishop"] = []
        black_locs["bishop"] = []
        white_locs["rook"] = []
        black_locs["rook"] = []
        white_locs["queen"] = []
        black_locs["queen"] = []
        white_locs["king"] = []
        black_locs["king"] = []
        for i in range(8):
            grid[1][i].add_piece("black", "pond", "images/blackPond.png", 1, i)
            grid[6][i].add_piece("white", "pond", "images/whitePond.png", 6, i)
            black_locs["pond"].append((1, i))
            white_locs["pond"].append((6, i))


        grid[0][0].add_piece("black", "rook", "images/blackRook.png", 0, 0)
        grid[0][7].add_piece("black", "rook", "images/blackRook.png", 0, 7)
        grid[7][0].add_piece("white", "rook", "images/whiteRook.png", 7, 0)
        grid[7][7].add_piece("white", "rook", "images/whiteRook.png", 7, 7)
        black_locs["rook"].append((0, 0))
        black_locs["rook"].append((0, 7))
        white_locs["rook"].append((7, 0))
        white_locs["rook"].append((7, 7))

        grid[0][1].add_piece("black", "knight", "images/blackKnight.png", 0, 1)
        grid[0][6].add_piece("black", "knight", "images/blackKnight.png", 0, 6)
        grid[7][1].add_piece("white", "knight", "images/whiteKnight.png", 7, 1)
        grid[7][6].add_piece("white", "knight", "images/whiteKnight.png", 7, 6)
        black_locs["knight"].append((0, 1))
        black_locs["knight"].append((0, 6))
        white_locs["knight"].append((7, 1))
        white_locs["knight"].append((7, 6))
        

        grid[0][2].add_piece("black", "bishop", "images/blackBishop.png", 0, 2)
        grid[0][5].add_piece("black", "bishop", "images/blackBishop.png", 0, 5)
        grid[7][2].add_piece("white", "bishop", "images/whiteBishop.png", 7, 2)
        grid[7][5].add_piece("white", "bishop", "images/whiteBishop.png", 7, 5)
        black_locs["bishop"].append((0, 2))
        black_locs["bishop"].append((0, 5))
        white_locs["bishop"].append((7, 2))
        white_locs["bishop"].append((7, 5))
        

        grid[0][3].add_piece("black", "queen", "images/blackQueen.png", 0, 3)
        grid[0][4].add_piece("black", "king", "images/blackKing.png", 0, 4)
        grid[7][3].add_piece("white", "queen", "images/whiteQueen.png", 7, 3)
        grid[7][4].add_piece("white", "king", "images/whiteKing.png", 7, 4)
        black_locs["queen"].append((0, 3))
        black_locs["king"].append((0, 4))
        white_locs["queen"].append((7, 3))
        white_locs["king"].append((7, 4))
        


    def moveAnimation(self, surface, original_locations, final_locations):       # for AI
        pass



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



    def get_moves(self, piece, row, col, team):
        self.row = row
        self.col = col
        self.team = team
        moves = []

        if (piece == "pond"):
            if (self.team == "white"):
                
                if (row == 6):
                    if (self.grid[row-1][col].piece == None):
                        moves.append([row-1, col])
                    if (self.grid[row-2][col].piece == None and self.grid[row-1][col].piece == None):
                        moves.append([row-2, col])
                    if (col >= 0 and col < COLS - 1):
                        if (self.grid[row-1][col+1].team == "black"):
                            moves.append([row-1, col+1])
                    if (col > 0 and col <= COLS - 1):
                        if (self.grid[row-1][col-1].team == "black"):
                            moves.append([row-1, col-1])
                    
                    
                if (row >= 1 and row <= 5):
                    if (self.grid[row-1][col].piece == None):
                        moves.append([row-1, col])

                if (row >= 1 and row <= 5 and col > 0 and col < COLS-1):  # Capturing
                    if (self.grid[row-1][col-1].team == "black"):
                        moves.append([row-1, col-1])
                    if (self.grid[row-1][col+1].team == "black"):
                        moves.append([row-1, col+1])
                

            elif (self.team == "black"):
                
                if (row == 1):
                    if (self.grid[row+1][col].piece == None):
                        moves.append([row+1, col])
                    if (self.grid[row+2][col].piece == None):
                        moves.append([row+2, col])
                    if (col >= 0 and col < COLS - 1):
                        if (self.grid[row+1][col+1].team == "white"):
                            moves.append([row+1, col+1])
                    if (col > 0 and col <= COLS - 1):
                        if (self.grid[row+1][col-1].team == "white"):
                            moves.append([row+1, col-1])
                    
                        
                if (row >= 2 and row <= 6):
                    if (self.grid[row+1][col].piece == None):
                        moves.append([row+1, col])

                if (row >= 2 and row <= 6 and col > 0 and col < COLS-1):  # Capturing
                    if (self.grid[row+1][col-1].team == "white"):
                        moves.append([row+1, col-1])
                    if (self.grid[row+1][col+1].team == "white"):
                        moves.append([row+1, col+1])


        ##########################################
        elif (piece == "bishop"):

            copy_row = self.row
            copy_col = self.col

            
            
            if (team == "white"):

                while (row > 0 and col > 0):
                    row = row - 1
                    col = col - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])

                    if (self.grid[row][col].piece != None or self.grid[row][col].team == "black"):
                        break

                row = copy_row
                col = copy_col
                while (row > 0 and col < COLS-1):
                    row = row - 1
                    col = col + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                    
                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col > 0):
                    row = row + 1
                    col = col - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col < COLS-1):
                    row = row + 1
                    col = col + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break

            elif(self.team == "black"):

                while (row > 0 and col > 0):
                    row = row - 1
                    col = col - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])

                    if (self.grid[row][col].piece != None or self.grid[row][col].team == "white"):
                        break

                row = copy_row
                col = copy_col
                while (row > 0 and col < COLS-1):
                    row = row - 1
                    col = col + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                    
                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col > 0):
                    row = row + 1
                    col = col - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col < COLS-1):
                    row = row + 1
                    col = col + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break

        
        ##########################################
        elif (piece == "knight"):

            

            if (self.team == "white"):
                if (row-2 >= 0 and col-1 >= 0):
                    if (self.grid[row-2][col-1].piece == None or self.grid[row-2][col-1].team == "black"):
                        moves.append([row-2, col-1])
                if (row-2 >= 0 and col+1 <= COLS-1):
                    if (self.grid[row-2][col+1].piece == None or self.grid[row-2][col+1].team == "black"):
                        moves.append([row-2, col+1])
                if (row-1 >= 0 and col-2 >= 0):
                    if (self.grid[row-1][col-2].piece == None or self.grid[row-1][col-2].team == "black"):
                        moves.append([row-1, col-2])
                if (row+1 <= ROWS-1 and col-2 >= 0):
                    if (self.grid[row+1][col-2].piece == None or self.grid[row+1][col-2].team == "black"):
                        moves.append([row+1, col-2])
                if (row+2 <= ROWS-1 and col-1 >= 0):
                    if (self.grid[row+2][col-1].piece == None or self.grid[row+2][col-1].team == "black"):
                        moves.append([row+2, col-1])
                if (row+2 <= ROWS-1 and col+1 <= COLS-1):
                    if (self.grid[row+2][col+1].piece == None or self.grid[row+2][col+1].team == "black"):
                        moves.append([row+2, col+1])
                if (row+1 <= ROWS-1 and col+2 <= COLS-1):
                    if (self.grid[row+1][col+2].piece == None or self.grid[row+1][col+2].team == "black"):
                        moves.append([row+1, col+2])
                if (row-1 >=0 and col+2 <= COLS-1):
                    if (self.grid[row-1][col+2].piece == None or self.grid[row-1][col+2].team == "black"):
                        moves.append([row-1, col+2])


            elif (self.team == "black"):
                if (row-2 >= 0 and col-1 >= 0):
                    if (self.grid[row-2][col-1].piece == None or self.grid[row-2][col-1].team == "white"):
                        moves.append([row-2, col-1])
                if (row-2 >= 0 and col+1 <= COLS-1):
                    if (self.grid[row-2][col+1].piece == None or self.grid[row-2][col+1].team == "white"):
                        moves.append([row-2, col+1])
                if (row-1 >= 0 and col-2 >= 0):
                    if (self.grid[row-1][col-2].piece == None or self.grid[row-1][col-2].team == "white"):
                        moves.append([row-1, col-2])
                if (row+1 <= ROWS-1 and col-2 >= 0):
                    if (self.grid[row+1][col-2].piece == None or self.grid[row+1][col-2].team == "white"):
                        moves.append([row+1, col-2])
                if (row+2 <= ROWS-1 and col-1 >= 0):
                    if (self.grid[row+2][col-1].piece == None or self.grid[row+2][col-1].team == "white"):
                        moves.append([row+2, col-1])
                if (row+2 <= ROWS-1 and col+1 <= COLS-1):
                    if (self.grid[row+2][col+1].piece == None or self.grid[row+2][col+1].team == "white"):
                        moves.append([row+2, col+1])
                if (row+1 <= ROWS-1 and col+2 <= COLS-1):
                    if (self.grid[row+1][col+2].piece == None or self.grid[row+1][col+2].team == "white"):
                        moves.append([row+1, col+2])
                if (row-1 >=0 and col+2 <= COLS-1):
                    if (self.grid[row-1][col+2].piece == None or self.grid[row-1][col+2].team == "white"):
                        moves.append([row-1, col+2])

        ##########################################
        elif (piece == "rook"):
            copy_row = self.row
            copy_col = self.col

            if team == "white":

                while (row > 0):
                    row = row - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                row = copy_row

                while (row < ROWS-1):
                    row = row + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                row = copy_row

                while (col > 0):
                    col = col - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                col = copy_col
                
                while (col < COLS-1):
                    col = col + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break

            elif team == "black":

                while (row > 0):
                    row = row - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                row = copy_row

                while (row < ROWS-1):
                    row = row + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                row = copy_row

                while (col > 0):
                    col = col - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                col = copy_col
                
                while (col < COLS-1):
                    col = col + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
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
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])

                    if (self.grid[row][col].piece != None or self.grid[row][col].team == "black"):
                        break

                row = copy_row
                col = copy_col
                while (row > 0 and col < COLS-1):
                    row = row - 1
                    col = col + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                    
                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col > 0):
                    row = row + 1
                    col = col - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col < COLS-1):
                    row = row + 1
                    col = col + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col

                ### horizontal moves
                while (row > 0):
                    row = row - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                row = copy_row

                while (row < ROWS-1):
                    row = row + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                row = copy_row

                while (col > 0):
                    col = col - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                col = copy_col
                
                while (col < COLS-1):
                    col = col + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                col = copy_col
            
            elif (team == "black"):
                
                while (row > 0 and col > 0):
                    row = row - 1
                    col = col - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])

                    if (self.grid[row][col].piece != None or self.grid[row][col].team == "white"):
                        break

                row = copy_row
                col = copy_col
                while (row > 0 and col < COLS-1):
                    row = row - 1
                    col = col + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                    
                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col > 0):
                    row = row + 1
                    col = col - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col
                while (row < ROWS-1 and col < COLS-1):
                    row = row + 1
                    col = col + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break

                row = copy_row
                col = copy_col

                while (row > 0):
                    row = row - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                row = copy_row

                while (row < ROWS-1):
                    row = row + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                row = copy_row

                while (col > 0):
                    col = col - 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                col = copy_col
                
                while (col < COLS-1):
                    col = col + 1
                    if (self.grid[row][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col])
                    if (self.grid[row][col].piece != None):
                        break
                col = copy_col

        ##########################################
        elif (piece == "king"):
            if team == "white":
                if (row > 0 and col > 0):
                    if (self.grid[row-1][col-1].piece == None or self.grid[row-1][col-1].team == "black"):
                        moves.append([row-1, col-1])
                    if (self.grid[row-1][col].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row-1, col])
                    if (self.grid[row][col-1].piece == None or self.grid[row][col].team == "black"):
                        moves.append([row, col-1])
                
                if (row < ROWS-1 and col < COLS-1):
                    if (self.grid[row+1][col+1].piece == None or self.grid[row+1][col+1].team == "black"):
                        moves.append([row+1, col+1])
                    if (self.grid[row+1][col].piece == None or self.grid[row+1][col].team == "black"):
                        moves.append([row+1, col])
                    if (self.grid[row][col+1].piece == None or self.grid[row][col+1].team == "black"):
                        moves.append([row, col+1])
                
                if (row > 0 and col < COLS-1):
                    if (self.grid[row-1][col+1].piece == None or self.grid[row-1][col+1].team == "black"):
                        moves.append([row-1, col+1])
                if (row < ROWS-1 and col > 0):
                    if (self.grid[row+1][col-1].piece == None or self.grid[row+1][col-1].team == "black"):
                        moves.append([row+1, col-1])
            
            elif team == "black":
                if (row > 0 and col > 0):
                    if (self.grid[row-1][col-1].piece == None or self.grid[row-1][col-1].team == "white"):
                        moves.append([row-1, col-1])
                    if (self.grid[row-1][col].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row-1, col])
                    if (self.grid[row][col-1].piece == None or self.grid[row][col].team == "white"):
                        moves.append([row, col-1])
                
                if (row < ROWS-1 and col < COLS-1):
                    if (self.grid[row+1][col+1].piece == None or self.grid[row+1][col+1].team == "white"):
                        moves.append([row+1, col+1])
                    if (self.grid[row+1][col].piece == None or self.grid[row+1][col].team == "white"):
                        moves.append([row+1, col])
                    if (self.grid[row][col+1].piece == None or self.grid[row][col+1].team == "white"):
                        moves.append([row, col+1])
                
                if (row > 0 and col < COLS-1):
                    if (self.grid[row-1][col+1].piece == None or self.grid[row-1][col+1].team == "white"):
                        moves.append([row-1, col+1])
                if (row < ROWS-1 and col > 0):
                    if (self.grid[row+1][col-1].piece == None or self.grid[row+1][col-1].team == "white"):
                        moves.append([row+1, col-1])
        
        return moves
    

    def check4Checks(self, copygrid, AttackingTeam):
        # check if black is in check
        
        inCheck = False
        if (AttackingTeam == "white"):
            
            # get king position
            kingloc = list(self.white_locs["king"])
            print("kingloc check", kingloc)
            

            for row in range(ROWS):
                for col in range(COLS):
                    if copygrid[row][col].team == "black":
                        piece = copygrid[row][col].piece
                        piece_moves = self.get_moves(piece, row, col, "black")
                        print("kingloc check", kingloc, "piece moves check", piece_moves)
                        if piece_moves.count(kingloc) >= 1:
                            inCheck = True
                            self.blackCheck = True
                            self.attackingWhiteforCheck.append([row, col])
            print("CHECK RESULT: ", inCheck)

            if len(self.attackingWhiteforCheck) == 0:
                inCheck = False
                self.blackCheck = False
            return inCheck
            
            #  def get_moves(self, piece, row, col, team):
            # need to keep track of all pieces
            pass
        
        
        if (AttackingTeam == "black"):
            pass

        #return True
        

# revealled check 
# check to position
# both

    def checkForChecks(self, attackingTeam):
        if attackingTeam == "white":
            pass

        elif attackingTeam == "black":
            pass
        
        
        
