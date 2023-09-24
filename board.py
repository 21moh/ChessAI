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
            grid[1][i].add_piece("black", "pond", "ChessAI/blackPond.png", 1, i)
            grid[6][i].add_piece("white", "pond", "ChessAI/whitePond.png", 6, i)
        
        grid[0][0].add_piece("black", "rook", "ChessAI/blackRook.png", 0, 0)
        grid[0][7].add_piece("black", "rook", "ChessAI/blackRook.png", 0, 7)
        grid[7][0].add_piece("white", "rook", "ChessAI/whiteRook.png", 7, 0)
        grid[7][7].add_piece("white", "rook", "ChessAI/whiteRook.png", 7, 7)

        grid[0][1].add_piece("black", "knight", "ChessAI/blackKnight.png", 0, 1)
        grid[0][6].add_piece("black", "knight", "ChessAI/blackKnight.png", 0, 6)
        grid[7][1].add_piece("white", "knight", "ChessAI/whiteKnight.png", 7, 1)
        grid[7][6].add_piece("white", "knight", "ChessAI/whiteKnight.png", 7, 6)

        grid[0][2].add_piece("black", "bishop", "ChessAI/blackBishop.png", 0, 2)
        grid[0][5].add_piece("black", "bishop", "ChessAI/blackBishop.png", 0, 5)
        grid[7][2].add_piece("white", "bishop", "ChessAI/whiteBishop.png", 7, 2)
        grid[7][5].add_piece("white", "bishop", "ChessAI/whiteBishop.png", 7, 5)

        grid[0][3].add_piece("black", "queen", "ChessAI/blackQueen.png", 0, 3)
        grid[0][4].add_piece("black", "king", "ChessAI/blackKing.png", 0, 4)
        grid[7][3].add_piece("white", "queen", "ChessAI/whiteQueen.png", 7, 3)
        grid[7][4].add_piece("white", "king", "ChessAI/whiteKing.png", 7, 4)
        
