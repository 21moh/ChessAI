import pygame
import sys

from const import *
from piece import Piece

class Square:
    def __init__(self, row, col):
        self.img = None
        self.team = None
        self.piece = None
        self.gridRow = row
        self.gridCol = col
        self.attakers = []
    
    def add_piece(self, team, piece, img, row, col):
        self.img = img
        self.team = team
        self.piece = piece
        self.gridRow = row
        self.gridCol = col
    
    def hasPiece(self):
        return self.piece != None
    
