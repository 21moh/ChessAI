import pygame
import sys

from const import *
from piece import Piece

class Board:
    def __init__(self):
        self.grid = [[None for i in range(8)] for i in range(8)]
        self.pieces = 