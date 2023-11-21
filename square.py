import pygame

from const import *

class Square:
    def __init__(self, row, col):
        self.piece = None
        self.team = None
        self.image = None
        self.row = row
        self.col = col
        self.moves = []
        self.whiteprotected = False
        self.blackprotected = False
        self.points = 0


    def setPoint(self):
        if (self.piece == "pond"):
            self.points = 1
        if (self.piece == "knight"):
            self.points = 3
        if (self.piece == "bishop"):
            self.points = 3
        if (self.points == "rook"):
            self.points = 5
        if (self.points == "queen"):
            self.points = 9
        if (self.points == "king"):
            self.points = 1000
    
    def add_piece(self, team, piece, img, row, col):
        self.piece = piece
        self.team = team
        self.image = img
        self.row = row
        self.col = col



    
    

    
