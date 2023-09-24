import pygame
import sys

from const import *

class Piece:
    def __init__(self, type, team, image, row, col):
        self.type = type
        self.team = team
        self.image = image
        self.row = row
        self.col = col
        self.connect = None
        self.possible_moves = []



