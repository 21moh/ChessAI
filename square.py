import pygame
import sys

from const import *

class Square:
    def __init__(self, row, col):
        self.piece = None
        self.gridRow = row
        self.gridCol = col
        self.attakers = []
    def add_piece(self, piece, row, col):
        self.piece = piece
        self.gridRow = row
        self.gridCol = col
    