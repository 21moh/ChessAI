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



    
    

    
