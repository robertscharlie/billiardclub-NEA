import pygame
import math
import random

pygame.init()

# Variables
FPS = 60
resolution = (1280, 720) # Screen dimensions
borderName = "Billiard Club" # Displays at the top of the program
VEC = pygame.math.Vector2
root3 = math.sqrt(3)
friction = 0.991
restitutionCoeff = 0.9

# friction = 1


# Table Variables and Setup
primaryTableColour = "#155843"
secondaryTableColour = "#313e46"
outerTableColour = "#313e46"

tableDimensions = (900,450)
centre = (resolution[0]//2, resolution[1]//2)
holeRadius = 15
ballRadius = 12

tableCorners = (
    (centre[0] - tableDimensions[0] / 2, centre[1] - tableDimensions[1] / 2), # Top Left
    (centre[0] + tableDimensions[0] / 2, centre[1] - tableDimensions[1] / 2), # Top Right
    (centre[0] - tableDimensions[0] / 2, centre[1] + tableDimensions[1] / 2), # Bottom Left
    (centre[0] + tableDimensions[0] / 2, centre[1] + tableDimensions[1] / 2), # Bottom Right
)

holePos = {
    "TL": (tableCorners[0][0]+1.1*holeRadius, tableCorners[0][1]+1.1*holeRadius), # Top Left
    "TR": (tableCorners[1][0]-1.1*holeRadius, tableCorners[0][1]+1.1*holeRadius), # Top Right
    "BL": (tableCorners[0][0]+1.1*holeRadius, tableCorners[2][1]-1.1*holeRadius), # Bottom Left
    "BR": (tableCorners[1][0]-1.1*holeRadius, tableCorners[2][1]-1.1*holeRadius), # Bottom Right
    "TM": (centre[0], tableCorners[0][1]+1.1*holeRadius), # Top Middle
    "BM": (centre[0], tableCorners[2][1]-1.1*holeRadius), # Bottom Middle
}

tableRails = {
        "TL": (
            (centre[0] - 1*holeRadius, tableCorners[0][1]),
            (centre[0] - 3*holeRadius, tableCorners[0][1]+1.5*holeRadius),
            (tableCorners[0][0] + 4*holeRadius, tableCorners[0][1]+1.5*holeRadius),
            (tableCorners[0][0] + 2*holeRadius, tableCorners[0][1]),
        ),

        "TR": (
            (centre[0] + 1*holeRadius, tableCorners[0][1]),
            (centre[0] + 3*holeRadius, tableCorners[0][1]+1.5*holeRadius),
            (tableCorners[1][0] - 4*holeRadius, tableCorners[0][1]+1.5*holeRadius),
            (tableCorners[1][0] - 2*holeRadius, tableCorners[0][1]),
        ),

        "BL": (
            (centre[0] - 1*holeRadius, tableCorners[2][1]-1),
            (centre[0] - 3*holeRadius, tableCorners[2][1]-1.5*holeRadius),
            (tableCorners[0][0] + 4*holeRadius, tableCorners[2][1]-1.5*holeRadius),
            (tableCorners[0][0] + 2*holeRadius, tableCorners[2][1]-1),
        ),

        "BR": (
            (centre[0] + 1*holeRadius, tableCorners[2][1]-1),
            (centre[0] + 3*holeRadius, tableCorners[2][1]-1.5*holeRadius),
            (tableCorners[1][0] - 4*holeRadius, tableCorners[2][1]-1.5*holeRadius),
            (tableCorners[1][0] - 2*holeRadius, tableCorners[2][1]-1),
            
        ),
        
        "ML": (
            (tableCorners[0][0], tableCorners[3][1] - 2*holeRadius),
            (tableCorners[0][0]+1.5*holeRadius, tableCorners[3][1] - 4*holeRadius),
            (tableCorners[0][0]+1.5*holeRadius, tableCorners[1][1] + 4*holeRadius),
            (tableCorners[0][0], tableCorners[1][1] + 2*holeRadius),
            
            
        ),
        
        "MR": (
            (tableCorners[1][0]-1, tableCorners[3][1] - 2*holeRadius),
            (tableCorners[1][0]-1.5*holeRadius, tableCorners[3][1] - 4*holeRadius),
            (tableCorners[1][0]-1.5*holeRadius, tableCorners[1][1] + 4*holeRadius),
            (tableCorners[1][0]-1, tableCorners[1][1] + 2*holeRadius),
            
            
        ),
    }

# Ball Class
class Ball(pygame.sprite.Sprite): # Defines a class for a ball
    def __init__(self, colour, radius, pos, velocity, mass): # Constructor Method
        super().__init__()
        self.colour = colour
        self.radius = radius
        self.pos = VEC(pos) # Position Vector
        self.velocity = VEC(velocity) # Velocity vector
        self.mass = mass

    def update(self): # Updates the position of the ball
        self.pos += self.velocity # moves ball to next position
        self.velocity *= friction # reduces the velocity of the ball
        
        # Checking collisions with the walls:
        
        if self.pos[0] - self.radius <= tableCorners[0][0]: # Left Wall
            self.pos[0] = self.radius + tableCorners[0][0]  # Put ball on edge of wall
            self.velocity[0] *= -1 # Reverses X component
        
        if self.pos[0] + self.radius >= tableCorners[1][0]: # Right Wall
            self.pos[0] = tableCorners[1][0] - self.radius # Put ball on edge of wall
            self.velocity[0] *= -1 # Reverses X component
        
        if self.pos[1] - self.radius <= tableCorners[0][1]: # Top Wall
            self.pos[1] = self.radius + tableCorners[0][1] # Put ball on edge of wall
            self.velocity[1] *= -1 # Reverses Y component
        
        if self.pos[1] + self.radius >= tableCorners[2][1]: # Bottom Wall
            self.pos[1] = tableCorners[2][1] - self.radius # Put ball on edge of wall
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

            self.velocity *= restitutionCoeff # decreases velocity of both balls
            other.velocity *= restitutionCoeff

            # Push out the colliding balls
            while distanceSquared < (self.radius + other.radius)**2:
                self.pos += n # move balls away from each other
                other.pos -= n
                distanceSquared = self.pos.distance_squared_to(other.pos) # distance squared between points

    def checkResolveWallCollision(self):
        # Loops through each of the Rails (where collisions should be done)
        for i in tableRails:
            for j in range(3):
                lineStart = tableRails[i][j] # Coordinates of the Line Start and End
                lineEnd = tableRails[i][j+1] # e.g. [ [x1,y1] , [x2,y2] ]
                lineVec = VEC(lineEnd[0] - lineStart[0], lineEnd[1] - lineStart[1]) # Vector of the Line
                circleVec = VEC(self.pos[0] - lineStart[0], self.pos[1] - lineStart[1]) # Vector of the circle to the start of the line
                t = max(0, min(1, (circleVec[0] * lineVec[0] + circleVec[1] * lineVec[1]) / lineVec.magnitude_squared()))
                # This creates a parameter that will calculate the s.f of the normal projection that maps the circle onto the line segment
                linePoint = (lineStart[0] + t * lineVec[0], lineStart[1] + t * lineVec[1]) # Calculate closest point on the line to the circle
                circlePointVec = VEC(linePoint[0] - self.pos[0], linePoint[1] - self.pos[1]) # Vector of the circle to the closest point
                distance = circlePointVec.magnitude() # calculates distance between the circle and closest point
                
                # Check if colliding
                if distance <= self.radius:
                    self.pos -= self.velocity # undoes previous update
                    n = circlePointVec.normalize() # creates a normal vector as a origin for calculations
                    impulse = 2 * (n * self.velocity) / (self.mass) # calculates the impulse the ball will get
                    self.velocity -= impulse * n # applies impulse to each ball
                    self.velocity *= restitutionCoeff # decreases velocity 

    def draw(self, screen): # Draws the ball to the screen
        pygame.draw.circle(screen, self.colour, self.pos, self.radius)

ballGroup = pygame.sprite.Group() # Groups all balls for easier maintenance

# Define where each ball should be relative to the start position
ballStartPos = {
    "white0":   (centre[0] - 20*ballRadius, centre[1]),
    "yellow1":  (centre[0] + 15*ballRadius, centre[1]),
    "blue2":    (centre[0] + 15*ballRadius + 1 * root3 * ballRadius, centre[1] + 1 * ballRadius),
    "red3":     (centre[0] + 15*ballRadius + 1 * root3 * ballRadius, centre[1] - 1 * ballRadius),
    "purple4":  (centre[0] + 15*ballRadius + 2 * root3 * ballRadius, centre[1] - 2 * ballRadius),
    "orange5":  (centre[0] + 15*ballRadius + 2 * root3 * ballRadius, centre[1] + 2 * ballRadius),
    "green6":   (centre[0] + 15*ballRadius + 3 * root3 * ballRadius, centre[1] - 1 * ballRadius,),
    "maroon7":  (centre[0] + 15*ballRadius + 3 * root3 * ballRadius, centre[1] + 1 * ballRadius),
    "black8":   (centre[0] + 15*ballRadius + 2 * root3 * ballRadius, centre[1]),
    "yellow9":  (centre[0] + 15*ballRadius + 3 * root3 * ballRadius, centre[1] - 3 * ballRadius),
    "blue10":   (centre[0] + 15*ballRadius + 3 * root3 * ballRadius, centre[1] + 3 * ballRadius),
    "red11":    (centre[0] + 15*ballRadius + 4 * root3 * ballRadius, centre[1] - 4 * ballRadius),
    "purple12": (centre[0] + 15*ballRadius + 4 * root3 * ballRadius, centre[1] - 2 * ballRadius),
    "orange13": (centre[0] + 15*ballRadius + 4 * root3 * ballRadius, centre[1]),
    "green14":  (centre[0] + 15*ballRadius + 4 * root3 * ballRadius, centre[1] + 2 * ballRadius),
    "maroon15": (centre[0] + 15*ballRadius + 4 * root3 * ballRadius, centre[1] + 4 * ballRadius),
}

# Instantiate each ball
balls = [
    Ball("white", ballRadius, ballStartPos["white0"], (30, 0), 1),      # Whiteball
    Ball("yellow", ballRadius, ballStartPos["yellow1"], (0, 0), 1),     # Yellow 1
    Ball("blue", ballRadius, ballStartPos["blue2"], (0, 0), 1),        # Blue 2
    Ball("red", ballRadius, ballStartPos["red3"], (0, 0), 1),           # Red 3
    Ball("purple", ballRadius, ballStartPos["purple4"], (0, 0), 1),    # Purple 4
    Ball("orange", ballRadius, ballStartPos["orange5"], (0, 0), 1),     # Orange 5
    Ball("green", ballRadius, ballStartPos["green6"], (0, 0), 1),       # Green 6
    Ball("maroon", ballRadius, ballStartPos["maroon7"], (0, 0), 1),     # Maroon 7
    Ball("black", ballRadius, ballStartPos["black8"], (0, 0), 1),      # Black 8
    Ball("yellow", ballRadius, ballStartPos["yellow9"], (0, 0), 1),     # Yellow 9
    Ball("blue", ballRadius, ballStartPos["blue10"], (0, 0), 1),       # Blue 10
    Ball("red", ballRadius, ballStartPos["red11"], (0, 0), 1),          # Red 11
    Ball("purple", ballRadius, ballStartPos["purple12"], (0, 0), 1),    # Purple 12
    Ball("orange", ballRadius, ballStartPos["orange13"], (0, 0), 1),    # Orange 13
    Ball("green", ballRadius, ballStartPos["green14"], (0, 0), 1),      # Green 14
    Ball("maroon", ballRadius, ballStartPos["maroon15"], (0, 0), 1),    # Maroon 15
]

for i in balls:
    ballGroup.add(i)


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

    # Outer Ring
    pygame.draw.rect(
        screen,
        outerTableColour,
        pygame.Rect(
            tableCorners[0][0]-20, tableCorners[0][1]-20,
            tableDimensions[0]+40, tableDimensions[1]+40
        ),
        15, # Width
        20  # Border Radius
    )

    # Draw Table
    pygame.draw.rect(
        screen,
        primaryTableColour, # Colour
        pygame.Rect(
            tableCorners[0][0], # Top Left x
            tableCorners[0][1], # Top Left y
            tableDimensions[0], # Width
            tableDimensions[1]  # Height
        ),
        border_radius=3 # Border Radius
    )

    
    # Draw Table Rails
    pygame.draw.polygon(screen, secondaryTableColour, tableRails["TL"])    # Top Left Side
    pygame.draw.polygon(screen, secondaryTableColour, tableRails["TR"])    # Top Right Side
    pygame.draw.polygon(screen, secondaryTableColour, tableRails["BL"])    # Bottom Left Side
    pygame.draw.polygon(screen, secondaryTableColour, tableRails["BR"])    # Bottom Right Side
    pygame.draw.polygon(screen, secondaryTableColour, tableRails["ML"])    # Left Middle Side
    pygame.draw.polygon(screen, secondaryTableColour, tableRails["MR"])    # Right Middle Side


    # Draw Holes
    for i in holePos:
        pygame.draw.circle(screen, "black", (holePos[i][0],holePos[i][1]), holeRadius)


    # Draws a white line on each of the Rails (where collisions should be done)
    for i in tableRails:
        for j in range(3):
            pygame.draw.line(screen, "white", tableRails[i][j],tableRails[i][j+1])


    ballGroup.update() # update each ball
    for ball in ballGroup.sprites():
        ball.checkResolveWallCollision() # checks wall collisions
        ball.draw(screen) # draws each ball

    # Checks collision between every pair of balls
    for i in range(len(ballGroup)):
        for j in range(i + 1, len(ballGroup)):
            ballGroup.sprites()[i].checkResolveCollision(ballGroup.sprites()[j])

    # FPS Display
    currentFPS = str(round(clock.get_fps(), 1))
    text = pygame.font.SysFont("dubaimedium", 20).render(
        (str(currentFPS)), True, "white")
    screen.blit(text, (5, 5))

    pygame.display.flip() # Updates the display
    clock.tick(FPS) # Caps the frame rate

