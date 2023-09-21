import pygame
import sys

from const import *
from piece import Piece

class Square:
    def __init__(self, row, col):
        self.piece = None
        self.team = None
        self.img = None
        self.object = None
        self.row = row
        self.col = col
        self.attakers = []
    
    def add_piece(self, team, piece, img, row, col):
        self.piece = piece
        self.team = team
        self.img = img
        self.row = row
        self.col = col
        self.object = Piece(self.piece, self.team, self.img, self.row, self.col)
    
