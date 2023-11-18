import pygame
import sys
import random
import copy

from const import *
from game import Game
from square import Square

from bardapi import Bard
import os
import time

import openai

openai.api_key = "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"


class Main:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Chess')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #, pygame.HWSURFACE
        self.game = Game()

    def mainloop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger

        #draw board while running

        running = True
        game.board.initialize_board()

        turn = "white"

        while running:
            game.show_board(screen)
            game.show_pieces(screen)
            game.board.loadProtections()

            if (self.game.board.blackInCheckmate == True):
                img = pygame.image.load("images/white wins.png")
                screen.blit(img, (-50, 100))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            if (self.game.board.whiteInCheckmate == True):
                img = pygame.image.load("images/black wins.png")
                screen.blit(img, (-50, 100))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            
            #  if turn == white     ->> HUMAN SECTION  

        #############################################     WHITE          #################################################################################################################
            #game.board.printProtections()
            
            if turn == "white":

                if dragger.dragging == True:
                    

                    clicked_row = dragger.mouseY // CELL_SIZE
                    clicked_col = dragger.mouseX // CELL_SIZE
                    # creates all possible move locations with piece
                    game.board.grid[dragger.initial_row][dragger.initial_col].moves = game.board.get_moves(dragger.piece.piece, dragger.initial_row, dragger.initial_col, dragger.piece.team, game.board.grid)
                    
                    # load all possible locations the piece can be placed
                    game.board.loadPlacements(game.board.grid[dragger.initial_row][dragger.initial_col].moves, turn, screen)
                    dragger.update_mouse(event.pos)
                    dragger.update_blit(screen)

                for event in pygame.event.get():
                    
                    if event.type == pygame.QUIT:
                        running = False  # Set the flag to exit the loop if the window is closed
                        pygame.quit()  # Quit Pygame properly
                        sys.exit()     # exit program quit game
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)
                        clicked_row = dragger.mouseY // CELL_SIZE
                        clicked_col = dragger.mouseX // CELL_SIZE
                        dragger.save_object(game.board.grid[clicked_row][clicked_col])
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(game.board.grid[clicked_row][clicked_col])        # gets specific piece on square 

                    if event.type == pygame.MOUSEBUTTONUP:
                        if dragger.piece != None:
                            clicked_row = dragger.mouseY // CELL_SIZE
                            clicked_col = dragger.mouseX // CELL_SIZE

                            game.board.checkChecker("black", game.board.grid) #--> attacking from black

                            
                            directions = game.board.CanCastle("white")
                            if len(directions) > 0:
                                if dragger.piece.piece == "king" and dragger.initial_row == 7 and dragger.initial_col == 4 and clicked_row == 7 and clicked_col == 7:
                                    game.board.Castle("white", "right")
                                    game.board.checkChecker("white", game.board.grid)
                                    turn = "black"
                                elif dragger.piece.piece == "king" and dragger.initial_row == 7 and dragger.initial_col == 4 and clicked_row == 7 and clicked_col == 0:
                                    game.board.Castle("white", "left")
                                    game.board.checkChecker("white", game.board.grid)
                                    turn = "black"


                            # checks if move is possible from the move list
                            result = (game.board.grid[dragger.initial_row][dragger.initial_col].moves).count([clicked_row, clicked_col])        # checks for valid placement

                            
                            if (clicked_row < ROWS and clicked_col < COLS and turn == "white" and dragger.piece.team == "white"):
                                if (result >= 1):                           # player drops piece into valid square

                                    if (self.game.board.whiteInCheck == False):

                                        copygrid = copy.deepcopy(game.board.grid)
                                        saveinitial = copy.deepcopy(game.board.grid[dragger.initial_row][dragger.initial_col])
                                        copygrid[clicked_row][clicked_col] = saveinitial
                                        copygrid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                        game.board.loadProtections2(copygrid)
                                        inCheck = game.board.checkChecker("black", copygrid)

                                        if inCheck == False:    # boolean prevents moving a friendly piece towards opening a check towards white king

                                            if dragger.piece.piece == "pond" and clicked_row == 0:     # transform pond into Queen
                                                game.board.grid[clicked_row][clicked_col] = Square(clicked_row, clicked_col)
                                                game.board.grid[clicked_row][clicked_col].add_piece("white", "queen", "images/whiteQueen.png", clicked_row, clicked_col)
                                                game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                game.board.checkChecker("white", game.board.grid)
                                                turn = "black"

                                            else:
                                                # shift all piece information into new Square and Piece for capture
                                                game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                game.board.grid[clicked_row][clicked_col].moves = []
                                                game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                turn = "black"
                                                if dragger.piece == 'king':
                                                    game.board.whiteKingLoc = [clicked_row, clicked_col]
                                                game.board.checkChecker("white", game.board.grid)
                                                        
                                    elif (self.game.board.whiteInCheck == True):
                                        for i in range(len(game.board.white_movable)):
                                            if game.board.white_move[i][0] == clicked_row and game.board.white_move[i][1] == clicked_col:
                                                x = game.board.white_move[i][0]
                                                y = game.board.white_move[i][1]
                                                if clicked_row == x and clicked_col == y:
                                                    game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                                                    game.board.grid[clicked_row][clicked_col].row = clicked_row
                                                    game.board.grid[clicked_row][clicked_col].col = clicked_col
                                                    game.board.grid[clicked_row][clicked_col].moves = []
                                                    game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)
                                                    game.board.grid[dragger.initial_row][dragger.initial_col].moves = []
                                                    game.board.white_movable = []
                                                    game.board.white_move = []
                                                    turn = "black"
                                                    game.board.checkChecker("white", game.board.grid)
                                                    if dragger.piece.piece == "king":
                                                        game.board.whiteKingLoc = [clicked_row, clicked_col]
                                            
                                                    break

                            dragger.dragging = False
                            dragger.piece = None
                            dragger.object = None
                            game.board.loadProtections()
                            if game.board.blackInCheck == True:
                                game.board.InCheckMoves("black")

                            


                
        ################################################    BLACK        ##############################################################################################################



            # if turn equals black --> AI SECTION
            elif turn == "black":

                def chatgpt(prompt, model="text-davinci-003"):
                    response = openai.Completion.create(
                        engine=model,
                        prompt=prompt,
                        max_tokens=100,
                        n=1,
                        stop=None,
                        temperature=0.5,
                    )

                    message = response.choices[0].text.strip()
                    return message

                time.sleep(2)
                input_text = """Hey Chatgpt, Can you play as black for me in this chess game? Here is the board currently:\n"""

                # use parallel processing when calling bard
                grid = game.board.grid
                input_text += "  01234567\n"
                for row in range(ROWS):
                    input_text += str(row)
                    input_text += " "
                    for col in range(COLS):
                        square = grid[row][col]
                        if square.piece == "rook" and square.team == "black":
                            input_text += "r"
                        if square.piece == "bishop" and square.team == "black":
                            input_text += "b"
                        if square.piece == "knight" and square.team == "black":
                            input_text += "n"
                        if square.piece == "queen" and square.team == "black":
                            input_text += "q"
                        if square.piece == "king" and square.team == "black":
                            input_text += "k"
                        if square.piece == "pond" and square.team == "black":
                            input_text += "p"
                        
                        if square.piece == "rook" and square.team == "white":
                            input_text += "R"
                        if square.piece == "bishop" and square.team == "white":
                            input_text += "B"
                        if square.piece == "knight" and square.team == "white":
                            input_text += "N"
                        if square.piece == "queen" and square.team == "white":
                            input_text += "Q"
                        if square.piece == "king" and square.team == "white":
                            input_text += "K"
                        if square.piece == "pond" and square.team == "white":
                            input_text += "P"
                        
                        elif square.piece == None:
                            input_text += "."
                    input_text += "\n"

                input_text += "Also, here are all the possible moves you can make assuming we are treating the board like a double list in python"
                if game.board.blackInCheck == False:
                    blackmoves = dict()
                    numMove = 1
                    for row in range(ROWS):
                        for col in range(COLS):
                            if grid[row][col].team == "black":
                                moves = game.board.get_moves(grid[row][col].piece, row, col, "black", grid)
                                for move in moves:
                                    piece = grid[row][col].piece
                                    input_text += "move "
                                    input_text += str(numMove)
                                    input_text += ": black"
                                    input_text += piece
                                    input_text += " at ["
                                    input_text += str(row)
                                    input_text += ", "
                                    input_text += str(col)
                                    input_text += "]"
                                    input_text += " to ["
                                    input_text += str(move[0])
                                    input_text += ", "
                                    input_text += str(move[1])
                                    input_text += "]\n"
                                    blackmoves[numMove] = [row, col, move[0], move[1]]
                                numMove += 1

                    directions = game.board.CanCastle("black")
                    rightCastle = False
                    leftCastle = False
                    if directions.count("right") >= 1:
                        rightCastle = True
                        input_text += "move "
                        input_text += str(numMove)
                        input_text += ": castle left direction"
                        input_text += "\n"
                        numMove += 1

                    if directions.count("left") >= 1:
                        leftCastle = True
                        input_text += "move "
                        input_text += str(numMove)
                        input_text += ": castle right direction"
                        input_text += "\n"
                        numMove += 1


                    input_text += "select your best move by simply returning the number value associated with the move you want to make. If your desired move is move 2, then simply reply with ONLY \"2\". It is important that you reply with ONLY the number value move you want to make, DO NOT say anything else, AND DO NOT explain your move. DO NOT CONVERSE WITH ME. Only text me the number value move you want to make"
                    input_text += "if there are no possible moves in the move list, reply with ONLY the value \"0\"."

                    response = chatgpt(input_text)
                    print("\n\n")
                    print("-----------")
                    print("line 298", response)
                    chosenNum = 1
                    buildValue = ""                    
                    for char in response:
                        if char.isdigit():
                            buildValue += char
                    buildValue = int(buildValue)
                    print("chosen num:", chosenNum)
                    print("num moves:", numMove)
                    moves = blackmoves[buildValue]      
                    initial = []
                    initial.append(moves[0])
                    initial.append(moves[1])
                    final = []
                    final.append(moves[2])
                    final.append(moves[3]) 
                    save = copy.deepcopy(grid[initial[0]][initial[1]])
                    grid[final[0]][final[1]] = save
                    grid[initial[0]][initial[1]]= Square(initial[0], initial[1])    

                elif game.board.blackInCheck == True:
                    blackmoves = dict()
                    numMove = 1
                    for i in range(len(game.board.black_movable)):
                        blackpiece = game.board.black_movable[i]
                        blackmoves[numMove] = [blackpiece.row, blackpiece.col, game.board.black_move[i][0], game.board.black_move[i][1]]
                        piece = blackpiece.piece
                        
                        input_text += "move "
                        input_text += str(numMove)
                        input_text += ": black"
                        input_text += piece
                        input_text += " at ["
                        input_text += str(blackpiece.row)
                        input_text += ", "
                        input_text += str(blackpiece.col)
                        input_text += "]"
                        input_text += " to ["
                        input_text += str(game.board.black_move[i][0])
                        input_text += ", "
                        input_text += str(game.board.black_move[i][1])
                        input_text += "]\n"
                        numMove += 1


                    input_text += "select your move by simply returning the number value associated with the move you want to make. If your desired move is move 2, then simply reply with ONLY \"2\". It is important that you reply with ONLY the number value move you want to make, DO NOT say anything else, AND DO NOT explain your move"


                    input_text += "if there are no possible moves in the move list, reply with ONLY the value \"0\"."


                    response = chatgpt(input_text)
                    print("line 345", response)
                    if response == "0":
                        game.board.blackInCheckmate = True
                    else:
                        chosenNum = None                    
                        for char in response:
                            if char.isdigit():
                                chosenNum = int(char)
                        moves = blackmoves[chosenNum]      
                        initial = []
                        initial.append(moves[0])
                        initial.append(moves[1])
                        final = []
                        final.append(moves[2])
                        final.append(moves[3]) 
                        save = copy.deepcopy(grid[initial[0]][initial[1]])
                        grid[final[0]][final[1]] = save
                        grid[initial[0]][initial[1]]= Square(initial[0], initial[1])    

                game.board.loadProtections()
                turn = "white"
                game.board.checkChecker("black", game.board.grid)
                if (game.board.whiteInCheck == True):
                    game.board.InCheckMoves("white")


                
                    

                    
                    


            pygame.display.flip()
    
    


    

main = Main()
main.mainloop()
