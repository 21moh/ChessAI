import pygame
import turtle

# Initialize Pygame
pygame.init()

# Set up the Pygame display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Turtle in Pygame")

# Create a Turtle object
t = turtle.Turtle()

# Set the Turtle's speed
t.speed(0)

# Draw a red square with the Turtle
t.color("red")
t.penup()
t.goto(-300, -200)
t.pendown()
t.forward(100)
t.right(90)
t.forward(100)
t.right(90)
t.forward(100)
t.right(90)
t.forward(100)
t.penup()

# Keep the Pygame window open until the user quits
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the Pygame window with white
    screen.fill((255, 255, 255))

    # Draw the Turtle graphics on the Pygame window
    t.hideturtle()
    screen.blit(t.getscreen().getbuffer(), (0, 0))

    # Update the Pygame display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
