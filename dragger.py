import pygame


from const import *

class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
        self.object = None          # Square class info object that is being dragged

    def update_blit(self, surface):
        piece = self.piece
        img = pygame.image.load(piece.image)

        original_width, original_height = img.get_size()

        spacing_factor = 0.9

        # Calculates scaling factors
        width_scale = CELL_SIZE * spacing_factor / original_width
        height_scale = CELL_SIZE * spacing_factor / original_height
        # Use the smaller scaling factor to maintain aspect ratio
        scale_factor = min(width_scale, height_scale)
        # Scales the image
        img = pygame.transform.scale(img, (int(original_width * scale_factor), int(original_height * scale_factor)))
        img_center = (self.mouseX, self.mouseY)
        surface.blit(img, img.get_rect(center=img_center))


        
        



    def save_object(self, obj):
        self.object = obj

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos # (xcoordinate, ycoordinate)

    def save_initial(self, pos):
        self.initial_row = pos[1] // CELL_SIZE
        self.initial_col = pos[0] // CELL_SIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False



    
