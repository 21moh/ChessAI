


if event.type == pygame.MOUSEBUTTONUP:
    dragger.dragging = False
    dragger.piece = None
    dragger.object = None
    # check for valid move:

    #if valid move -->
    clicked_row = dragger.mouseY // CELL_SIZE
    clicked_col = dragger.mouseX // CELL_SIZE

    game.board.grid[dragger.initial_row][dragger.initial_col].get_moves()               # gets all possible moves for piece
    possible_moves = game.board.grid[dragger.initial_row][dragger.initial_col].moves    # returns list of all possible moves for piece
    
    # add code here to check for piece blockings

    for i in range(len(possible_moves)):
        if (game.board.grid[possible_moves[i][0]][possible_moves[i][1]] != None):
            
    
    result = possible_moves.count([clicked_row, clicked_col])

    if (clicked_row < ROWS and clicked_col < COLS):


        if game.board.grid[clicked_row][clicked_col].piece == None and clicked_row < ROWS and clicked_col < COLS:

            # check if move is valid
            
            print(possible_moves)
            print(result)
            if result >= 1:

                # put clicked object in new location
                

                # copy all piece information into new Square and Piece
                game.board.grid[clicked_row][clicked_col] = game.board.grid[dragger.initial_row][dragger.initial_col]
                game.board.grid[clicked_row][clicked_col].row = clicked_row
                game.board.grid[clicked_row][clicked_col].col = clicked_col
                game.board.grid[clicked_row][clicked_col].moves = []
                game.board.grid[dragger.initial_row][dragger.initial_col] = Square(dragger.initial_row, dragger.initial_col)

        

                print(game.board.grid[clicked_row][clicked_col].piece)
                
                game.show_board(screen)
                game.show_pieces(screen)

            game.board.grid[dragger.initial_row][dragger.initial_col].moves = []