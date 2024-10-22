import pygame

pygame.init()

# Variables
FPS = 60
resolution = (1000, 600) # Screen dimensions
borderName = "ballPhysics.py" # Displays at the top of the program
VEC = pygame.math.Vector2

# Pygame Functions
pygame.display.set_caption(borderName)
screen = pygame.display.set_mode(resolution) # Sets up the display
clock = pygame.time.Clock()

class Ball(pygame.sprite.Sprite): # Defines a class for a ball
    def __init__(self, colour, radius, pos, direction, speed): # Constructor Method
        super().__init__()
        self.colour = colour
        self.radius = radius
        self.pos = VEC(pos) # Position Vector
        self.direction = VEC(direction).normalize() # Normalised direction Vector 
        self.speed = speed # Initial speed of the ball
    
    def update(self): # Updates the position of the ball
        self.pos += self.direction * self.speed

    def draw(self, screen): # Draws the ball to the screen
        pygame.draw.circle(screen, self.colour, self.pos, self.radius)

ballGroup = pygame.sprite.Group() # Groups all balls for easier maintenance

ball1 = Ball("white", 10, (300,300), (1,0), 3) # Instantiates the Class
ballGroup.add(ball1) # Adds the ball to the group

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Checks if user closes program
            pygame.quit()
            exit()

    screen.fill((30, 30, 30)) # Fills the screen with a grey colour

    ballGroup.update()
    for ball in ballGroup.sprites():
        ball.draw(screen)

    pygame.display.flip() # Updates the display
    clock.tick(FPS) # Caps the frame rate