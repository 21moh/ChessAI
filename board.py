import pygame
import sys

from const import *
from piece import Piece
from square import Square

class Board:
    def __init__(self):
        self.grid = [[None for i in range(8)] for i in range(8)]    #square class, holds current piece and possible attacking pieces
        
    def initialize_board(self):
        grid = self.grid
        for i in range(ROWS):
            for j in range(COLS):
                grid[i][j] = Square(i, j)
        
        for i in range(8):
            grid[1][i].add_piece("black", "pond", "blackPond.png", 1, i)
            grid[6][i].add_piece("white", "pond", "whitePond.png", 6, i)
        
        grid[0][0].add_piece("black", "rook", "blackRook.png", 0, 0)
        grid[0][7].add_piece("black", "rook", "blackRook.png", 0, 7)
        grid[7][0].add_piece("white", "rook", "whiteRook.png", 7, 0)
        grid[7][7].add_piece("white", "rook", "whiteRook.png", 7, 7)

        grid[0][1].add_piece("black", "knight", "blackKnight.png", 0, 1)
        grid[0][6].add_piece("black", "knight", "blackKnight.png", 0, 6)
        grid[7][1].add_piece("white", "knight", "whiteKnight.png", 7, 1)
        grid[7][6].add_piece("white", "knight", "whiteKnight.png", 7, 6)

        grid[0][2].add_piece("black", "bishop", "blackBishop.png", 0, 2)
        grid[0][5].add_piece("black", "bishop", "blackBishop.png", 0, 5)
        grid[7][2].add_piece("white", "bishop", "whiteBishop.png", 7, 2)
        grid[7][5].add_piece("white", "bishop", "whiteBishop.png", 7, 5)

        grid[0][3].add_piece("black", "queen", "blackQueen.png", 0, 3)
        grid[0][4].add_piece("black", "king", "blackKing.png", 0, 4)
        grid[7][3].add_piece("white", "queen", "whiteQueen.png", 7, 3)
        grid[7][4].add_piece("white", "king", "whiteKing.png", 7, 4)


    def capture(self, piece):
        pass

    def get_moves(self, piece, row, col, team):
        self.row = row
        self.col = col
        self.team = team
        moves = []

        if (piece == "pond"):
            if (self.team == "white"):
                
                if (row == 6):
                    moves.append([row-2, col])
                    moves.append([row-1, col])
                if (row >= 1 and row <= 5):
                    moves.append([row-1, col])
                if (row >= 1 and row <= 5 and col > 0 and col < COLS):  # Capturing
                    if (self.grid[row-1][col-1].piece != None):
                        moves.append([row-1, col-1])
                    if (self.grid[row-1][col+1].piece != None):
                        moves.append([row-1, col+1])
                

            elif (self.team == "black"):
                if (row == 1):
                    moves.append([row+2, col])
                    moves.append([row+1, col])
                elif (row >= 2 and row <= 6):
                    moves.append([row+1, col])


        ##########################################
        elif (piece == "bishop"):

            copy_row = self.row
            copy_col = self.col

            while (row > 0 and col > 0):
                row = row - 1
                col = col - 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break

            row = copy_row
            col = copy_col
            while (row > 0 and col < COLS-1):
                row = row - 1
                col = col + 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break
                
            row = copy_row
            col = copy_col
            while (row < ROWS-1 and col > 0):
                row = row + 1
                col = col - 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break

            row = copy_row
            col = copy_col
            while (row < ROWS-1 and col < COLS-1):
                row = row + 1
                col = col + 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break

            row = copy_row
            col = copy_col

            if (self.team == "white"):
                pass

            elif(self.team == "black"):
                pass

        
        ##########################################
        elif (piece == "knight"):

            if (row-2 >= 0 and col-1 >= 0):
                moves.append([row-2, col-1])
            if (row-2 >= 0 and col+1 <= COLS-1):
                moves.append([row-2, col+1])
            if (row-1 >= 0 and col-2 >= 0):
                moves.append([row-1, col-2])
            if (row+1 <= ROWS-1 and col-2 >= 0):
                moves.append([row+1, col-2])
            if (row+2 <= ROWS-1 and col-1 >= 0):
                moves.append([row+2, col-1])
            if (row+2 <= ROWS-1 and col+1 <= COLS-1):
                moves.append([row+2, col+1])
            if (row+1 <= ROWS-1 and col+2 <= COLS-1):
                moves.append([row+1, col+2])
            if (row-1 >=0 and col+2 <= COLS-1):
                moves.append([row-1, col+2])

            if (self.team == "white"):
                pass

        ##########################################
        elif (piece == "rook"):
            copy_row = self.row
            copy_col = self.col

            while (row > 0):
                row = row - 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break
            row = copy_row

            while (row < ROWS-1):
                row = row + 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break
            row = copy_row

            while (col > 0):
                col = col - 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break
            col = copy_col
            
            while (col < COLS-1):
                col = col + 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break
            col = copy_col


        ##########################################
        elif (piece == "queen"):
            copy_row = self.row
            copy_col = self.col

            while (row > 0 and col > 0):
                row = row - 1
                col = col - 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break

            row = copy_row
            col = copy_col
            while (row > 0 and col < COLS-1):
                row = row - 1
                col = col + 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break
                
            row = copy_row
            col = copy_col
            while (row < ROWS-1 and col > 0):
                row = row + 1
                col = col - 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break

            row = copy_row
            col = copy_col
            while (row < ROWS-1 and col < COLS-1):
                row = row + 1
                col = col + 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break

            row = copy_row
            col = copy_col

            while (row > 0):
                row = row - 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break
            row = copy_row

            while (row < ROWS-1):
                row = row + 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break
            row = copy_row

            while (col > 0):
                col = col - 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break
            col = copy_col
            
            while (col < COLS-1):
                col = col + 1
                moves.append([row, col])
                if (self.grid[row][col].piece != None):
                    break
            col = copy_col


        ##########################################
        elif (piece == "king"):
            if (row > 0 and col > 0):
                moves.append([row-1, col-1])
                moves.append([row-1, col])
                moves.append([row, col-1])
            if (row < ROWS and col < COLS):
                moves.append([row+1, col+1])
                moves.append([row+1, col])
                moves.append([row, col+1])
            if (row > 0 and col < COLS):
                moves.append([row-1, col+1])
            if (row < ROWS and col > 0):
                moves.append([row+1, col-1])
        
        return moves
