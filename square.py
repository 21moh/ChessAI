import pygame

from const import *

class Square:
    def __init__(self, row, col):
        self.piece = None
        self.team = None
        self.image = None
        self.row = row
        self.col = col
        #self.attakers = []
        self.moves = []
    
    def add_piece(self, team, piece, img, row, col):
        self.piece = piece
        self.team = team
        self.image = img
        self.row = row
        self.col = col


    def get_moves(self):
        piece = self.piece
        row = self.row
        col = self.col


        ##########################################
        if (piece == "pond"):
            if (self.team == "white"):
                
                if (row == 6):
                    self.moves.append([row-2, col])
                    self.moves.append([row-1, col])
                elif (row >= 1 and row <= 5):
                    self.moves.append([row-1, col])
                

            elif (self.team == "black"):
                if (row == 1):
                    self.moves.append([row+2, col])
                    self.moves.append([row+1, col])
                elif (row >= 2 and row <= 6):
                    self.moves.append([row+1, col])


        ##########################################
        elif (piece == "bishop"):

            copy_row = self.row
            copy_col = self.col

            while (row > 0 and col > 0):
                self.moves.append([row-1,col-1])
                row = row - 1
                col = col - 1

            row = copy_row
            col = copy_col
            while (row > 0 and col < COLS):
                self.moves.append([row-1, col+1])
                row = row - 1
                col = col + 1
                
            row = copy_row
            col = copy_col
            while (row < ROWS and col > 0):
                self.moves.append([row+1, col-1])
                row = row + 1
                col = col - 1

            row = copy_row
            col = copy_col
            while (row < ROWS and col < COLS):
                self.moves.append([row+1, col+1])
                row = row + 1
                col = col + 1

            row = copy_row
            col = copy_col

            if (self.team == "white"):
                pass

            elif(self.team == "black"):
                pass

        
        ##########################################
        elif (piece == "knight"):

            if (row-2 >= 0 and col-1 >= 0):
                    self.moves.append([row-2, col-1])
            if (row-2 >= 0 and col+1 <= COLS-1):
                self.moves.append([row-2, col+1])
            if (row-1 >= 0 and col-2 >= 0):
                self.moves.append([row-1, col-2])
            if (row+1 <= ROWS-1 and col-2 >= 0):
                self.moves.append([row+1, col-2])
            if (row+2 <= ROWS-1 and col-1 >= 0):
                self.moves.append([row+2, col-1])
            if (row+2 <= ROWS-1 and col+1 <= COLS-1):
                self.moves.append([row+2, col+1])
            if (row+1 <= ROWS-1 and col+2 <= COLS-1):
                self.moves.append([row+1, col+2])
            if (row-1 >=0 and col+2 <= COLS-1):
                self.moves.append([row-1, col+2])

            if (self.team == "white"):
                pass

        ##########################################
        elif (piece == "rook"):
            copy_row = self.row
            copy_col = self.col

            while (row > 0):
                self.moves.append([row-1, col])
                row = row - 1
            row = copy_row

            while (row < ROWS):
                self.moves.append([row+1, col])
                row = row + 1
            row = copy_row

            while (col > 0):
                self.moves.append([row, col-1])
                col = col - 1
            col = copy_col

            while (col < COLS):
                self.moves.append([row, col+1])
                col = col + 1
            col = copy_col


        ##########################################
        elif (piece == "queen"):
            copy_row = self.row
            copy_col = self.col

            while (row > 0 and col > 0):
                self.moves.append([row-1,col-1])
                row = row - 1
                col = col - 1

            row = copy_row
            col = copy_col
            while (row > 0 and col < COLS):
                self.moves.append([row-1, col+1])
                row = row - 1
                col = col + 1
                
            row = copy_row
            col = copy_col
            while (row < ROWS and col > 0):
                self.moves.append([row+1, col-1])
                row = row + 1
                col = col - 1

            row = copy_row
            col = copy_col
            while (row < ROWS and col < COLS):
                self.moves.append([row+1, col+1])
                row = row + 1
                col = col + 1

            row = copy_row
            col = copy_col

            while (row > 0):
                self.moves.append([row-1, col])
                row = row - 1
            row = copy_row

            while (row < ROWS):
                self.moves.append([row+1, col])
                row = row + 1
            row = copy_row

            while (col > 0):
                self.moves.append([row, col-1])
                col = col - 1
            col = copy_col

            while (col < COLS):
                self.moves.append([row, col+1])
                col = col + 1
            col = copy_col


        ##########################################
        elif (piece == "king"):
            if (row > 0 and col > 0):
                self.moves.append([row-1, col-1])
                self.moves.append([row-1, col])
                self.moves.append([row, col-1])
            if (row < ROWS and col < COLS):
                self.moves.append([row+1, col+1])
                self.moves.append([row+1, col])
                self.moves.append([row, col+1])
            if (row > 0 and col < COLS):
                self.moves.append([row-1, col+1])
            if (row < ROWS and col > 0):
                self.moves.append([row+1, col-1])
                


    
    

    
