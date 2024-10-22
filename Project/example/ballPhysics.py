import pygame
import math
import random

pygame.init()

# Variables
FPS = 120
resolution = (800, 600) # Screen dimensions
borderName = "ballPhysics.py" # Displays at the top of the program
VEC = pygame.math.Vector2

ballRadius = 30

# Pygame Functions
pygame.display.set_caption(borderName)
screen = pygame.display.set_mode(resolution) # Sets up the display
clock = pygame.time.Clock()

class Ball(pygame.sprite.Sprite): # Defines a class for a ball
    def __init__(self, colour, radius, pos, velocity, mass): # Constructor Method
        super().__init__()
        self.colour = colour
        self.radius = radius
        self.pos = VEC(pos) # Position Vector
        self.velocity = VEC(velocity) # Velocity vector
        self.mass = mass

    def update(self): # Updates the position of the ball
        self.pos += self.velocity
        
        # Checking collisions with the walls:
        
        if self.pos[0] - self.radius <= 0: # Left Wall
            self.pos[0] = self.radius # Put ball on edge of wall
            self.velocity[0] *= -1 # Reverses X component
        
        if self.pos[0] + self.radius >= resolution[0]: # Right Wall
            self.pos[0] = resolution[0] - self.radius # Put ball on edge of wall
            self.velocity[0] *= -1 # Reverses X component
        
        if self.pos[1] - self.radius <= 0: # Top Wall
            self.pos[1] = self.radius # Put ball on edge of wall
            self.velocity[1] *= -1 # Reverses Y component
        
        if self.pos[1] + self.radius >= resolution[1]: # Bottom Wall
            self.pos[1] = resolution[1] - self.radius # Put ball on edge of wall
            self.velocity[1] *= -1 # Reverses Y component

    def checkResolveCollision(self, other): # Check if balls are colliding, then resolves collision
        # Check if balls colliding
        posDifference = self.pos - other.pos # find difference in positions
        distanceSquared = self.pos.distance_squared_to(other.pos) # distance squared between points

        if distanceSquared == 0: # prevents normalisation error
            return

        if distanceSquared < (self.radius + other.radius)**2: # If colliding
            self.pos -= self.velocity # undoes last move, to prevent clipping

            # Calculate Velocities after collision
            n = VEC(posDifference).normalize() # creates a normalised vector as a origin for calculations
            relVel = self.velocity - other.velocity # calculates the relative velocity of the balls
            impulse = 2 * (n * relVel) / (self.mass + other.mass) # calculates the impulse each ball will get
            
            self.velocity -= impulse * other.mass * n # applies impulse to each ball
            other.velocity += impulse * self.mass * n

            # Push out the colliding balls
            while distanceSquared < (self.radius + other.radius)**2:
                self.pos += n # move balls away from each other
                other.pos -= n
                distanceSquared = self.pos.distance_squared_to(other.pos) # distance squared between points

    def draw(self, screen): # Draws the ball to the screen
        pygame.draw.circle(screen, self.colour, self.pos, self.radius)

ballGroup = pygame.sprite.Group() # Groups all balls for easier maintenance

balls = [
    Ball("blue", radius=ballRadius, pos=(300,800), velocity=3*VEC(-1,5).normalize(), mass=5),# Instantiates the Class
    Ball("green", radius=ballRadius, pos=(100,300), velocity=3*VEC(6,5).normalize(), mass=5),
    Ball("yellow", radius=ballRadius, pos=(100,400), velocity=3*VEC(-1,5).normalize(), mass=5), 
]

for ball in balls:  
    ballGroup.add(ball) # Adds the ball to the group



count = 5
# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Checks if user closes program
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            ballGroup.add(
                Ball(
                    random.choice(["red", "green", "yellow", "blue"]),
                    ballRadius,
                    pygame.mouse.get_pos(),
                    (
                        random.choice([-1, 1]) * 3*random.random(),
                        random.choice([-1, 1]) * 3*random.random(),
                    ),
                    5,
                )
            )
            count += 1
    screen.fill((30, 30, 30)) # Fills the screen with a grey colour

    ballGroup.update() # update each ball
    for ball in ballGroup.sprites():
        ball.draw(screen) # draws each ball

    # Checks collision between every pair of balls
    for i in range(len(ballGroup)):
        for j in range(i + 1, len(ballGroup)):
            ballGroup.sprites()[i].checkResolveCollision(ballGroup.sprites()[j])

    # FPS Display
    currentFPS = str(round(clock.get_fps(), 1))
    text = pygame.font.SysFont("dubaimedium", 20).render(
        (str(currentFPS) + "  Balls: " + str(count)), True, "white", "black")
    screen.blit(text, (5, 5))

    pygame.display.flip() # Updates the display
    clock.tick(FPS) # Caps the frame rate