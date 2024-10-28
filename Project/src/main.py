import pygame

pygame.init()

# Variables
FPS = 60
resolution = (1280, 720) # Screen dimensions
borderName = "Billiard Club" # Displays at the top of the program



# Table Variables and Setup
tableDimensions = (1024,512)
centre = (resolution[0]/2, resolution[1]/2)
holeRadius = 14


tableCorners = (
    (centre[0] - tableDimensions[0] / 2, centre[1] - tableDimensions[1] / 2), # Top Left
    (centre[0] + tableDimensions[0] / 2, centre[1] - tableDimensions[1] / 2), # Top Right
    (centre[0] - tableDimensions[0] / 2, centre[1] + tableDimensions[1] / 2), # Bottom Left
    (centre[0] + tableDimensions[0] / 2, centre[1] + tableDimensions[1] / 2), # Bottom Right
)

holePos = {
    "TL": (tableCorners[0][0]+holeRadius, tableCorners[0][1]+holeRadius), # Top Left
    "TR": (tableCorners[1][0]-holeRadius, tableCorners[0][1]+holeRadius), # Top Right
    "BL": (tableCorners[0][0]+holeRadius, tableCorners[2][1]-holeRadius), # Bottom Left
    "BR": (tableCorners[1][0]-holeRadius, tableCorners[2][1]-holeRadius), # Bottom Right
    "TM": (centre[0], tableCorners[0][1]+holeRadius), # Top Middle
    "BM": (centre[0], tableCorners[2][1]-holeRadius), # Bottom Middle
}


# Pygame Functions
pygame.display.set_caption(borderName)
screen = pygame.display.set_mode(resolution) # Sets up the display
clock = pygame.time.Clock()

for i in holePos:
    print(i)


# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Checks if user closes program
            pygame.quit()
            exit()

    screen.fill((30, 30, 30)) # Fills the screen with a grey colour


    # Draw Table
    pygame.draw.rect(
        screen,
        "darkgreen", # Colour
        pygame.Rect(
            tableCorners[0][0], # Top Left x
            tableCorners[0][1], # Top Left y
            tableDimensions[0], # Width
            tableDimensions[1]  # Height
        )
    )

    # Draw Holes
    for i in holePos:
        pygame.draw.circle(screen, "white", (holePos[i][0],holePos[i][1]), holeRadius)


    pygame.display.flip() # Updates the display
    clock.tick(FPS) # Caps the frame rate

