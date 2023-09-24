import pygame
import sys

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
                
                
                #if board[row][grid] diagonal is opposite piece... --> restudy your code.

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
            

            if (self.team == "white"):
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
            pass


        ##########################################
        elif (piece == "queen"):
            pass


        ##########################################
        elif (piece == "king"):
            pass


    
    

    
