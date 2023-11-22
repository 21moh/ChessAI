
""""""
import pygame
import time

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Slow Moving Object")

# Load an image for the object
ball_image = pygame.image.load("images/whiteQueen.png")

original_width, original_height = ball_image.get_size()

spacing_factor = 0.9

# Calculates scaling factors
width_scale = 100 * spacing_factor / original_width
height_scale = 100 * spacing_factor / original_height
# Use the smaller scaling factor to maintain aspect ratio
scale_factor = min(width_scale, height_scale)
# Scales the image
ball_image = pygame.transform.scale(ball_image, (int(original_width * scale_factor), int(original_height * scale_factor)))
ball_rect = ball_image.get_rect(center=(400, 300))

# Define the object's speed
speed = 1

# Game loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the object
    ball_rect.x += speed
    ball_rect.y += speed

    # Keep the object within the screen boundaries
    if ball_rect.left <= 0:
        ball_rect.left = 300
    if ball_rect.right >= 800:
        ball_rect.right = 400
    if ball_rect.top <= 0:
        ball_rect.top = 300
    if ball_rect.bottom >= 600:
        ball_rect.bottom = 400

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the object
    screen.blit(ball_image, ball_rect)

    # Update the display
    pygame.display.flip()
    time.sleep(0.001)
    # Slow down the game loop
    # time.delay(10)

# Quit Pygame
pygame.quit()

