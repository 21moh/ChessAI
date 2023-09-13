import pygame
import sys



grid = [[' ' for i in range(8)] for i in range(8)]


class Piece:
    def __init__(self, team, type, image):
        self.team = team
        self.piece = type
        self.image = image

        # def move(piece)


def create_board(grid):
    for i in range(8):
        grid[1][i] = Piece("black", "pond", "blackPond.png")
        grid[6][i] = Piece("white", "pond", "whitePond.png")

    grid[0][0] = Piece("black", "rook", "blackRook.png")
    grid[0][7] = Piece("black", "rook", "blackRook.png")
    grid[7][0] = Piece("white", "rook", "whiteRook.png")
    grid[7][7] = Piece("white", "rook", "whiteRook.png")

    grid[0][1] = Piece("black", "knight", "blackKnight.png")
    grid[0][6] = Piece("black", "knight", "blackKnight.png")
    grid[7][1] = Piece("white", "knight", "whiteKnight.png")
    grid[7][6] = Piece("white", "knight", "whiteKnight.png")

    grid[0][2] = Piece("black", "bishop", "blackBishop.png")
    grid[0][5] = Piece("black", "bishop", "blackBishop.png")
    grid[7][2] = Piece("white", "bishop", "whiteBishop.png")
    grid[7][5] = Piece("white", "bishop", "whiteBishop.png")

    grid[0][3] = Piece("black", "queen", "blackQueen.png")
    grid[0][4] = Piece("black", "king", "blackKing.png")
    grid[7][3] = Piece("white", "queen", "whiteQueen.png")
    grid[7][4] = Piece("white", "king", "whiteKing.png")
    
    return grid


# main code

# Initialize Pygame
pygame.init()

# Define constants for the screen dimensions and cell size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
CELL_SIZE = SCREEN_WIDTH // 8

# Create the Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define your Piece class and create_board function here (same as in your code)

# Create the board and load piece images
create_board(grid)


spacing_factor = 0.9

# Load piece images
for row in grid:
    for piece in row:
        if piece != ' ':
            original_image = pygame.image.load(piece.image)
            original_width, original_height = original_image.get_size()

            # Calculate the scaling factors
            width_scale = CELL_SIZE * spacing_factor / original_width
            height_scale = CELL_SIZE * spacing_factor / original_height

            # Use the smaller scaling factor to maintain aspect ratio
            scale_factor = min(width_scale, height_scale)

            # Scale the image
            piece.image = pygame.transform.scale(original_image, (int(original_width * scale_factor), int(original_height * scale_factor)))

# Main game loop
running = True
while running:  #frames
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((200, 200, 200))  # White background

    # Draw the grid and pieces
    for row in range(8):
        for col in range(8):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            pygame.draw.rect(screen, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 1)  # Draw grid lines
            piece = grid[row][col]
            if piece != ' ':
                img_x = x + (CELL_SIZE - piece.image.get_width()) // 2
                img_y = y + (CELL_SIZE - piece.image.get_height()) // 2
                screen.blit(piece.image, (img_x, img_y))

    pygame.display.flip()

    

# Quit Pygame
pygame.quit()
sys.exit()