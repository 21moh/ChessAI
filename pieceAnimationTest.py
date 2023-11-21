import pygame
import time

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Moving Object")

# Load the image
image = pygame.image.load("images/whiteQueen.png")
original_width, original_height = image.get_size()

# Calculate scaling factors
spacing_factor = 0.9
width_scale = 100 * spacing_factor / original_width
height_scale = 100 * spacing_factor / original_height

# Use the smaller scaling factor to maintain aspect ratio
scale_factor = min(width_scale, height_scale)

# Scale the image
scaled_image = pygame.transform.scale(image, (int(original_width * scale_factor), int(original_height * scale_factor)))

# Initialize the object's position
object_x = 100
object_y = 100

# Set up the clock to limit the frame rate
clock = pygame.time.Clock()
fps = 60

# Game loop
running = True

while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the object's position
    object_x += 1

    # Draw the scaled image at the updated position
    screen.blit(scaled_image, (object_x, object_y))  # Update the position

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()

