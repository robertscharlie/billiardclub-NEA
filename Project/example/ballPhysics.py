import pygame

pygame.init()

# Variables
FPS = 60
resolution = (1000, 600) # Screen dimensions
borderName = "ballPhysics.py" # Displays at the top of the program

# Pygame Functions
pygame.display.set_caption(borderName)
screen = pygame.display.set_mode(resolution) # Sets up the display
clock = pygame.time.Clock()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Checks if user closes program
            pygame.quit()
            exit()

    screen.fill((30, 30, 30)) # Fills the screen with a grey colour

    pygame.display.flip() # Updates the display
    clock.tick(FPS) # Caps the frame rate