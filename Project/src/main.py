import pygame
import math

pygame.init()

# Variables
FPS = 70
resolution = (1280, 720) # Screen dimensions
borderName = "Billiard Club" # Displays at the top of the program
VEC = pygame.math.Vector2
root3 = math.sqrt(3)
friction = 0.991
restitutionCoeff = 0.95

# Table Variables and Setup
primaryTableColour = "#155843"
secondaryTableColour = "#313e46"
outerTableColour = "#313e46"
tableDimensions = (900,450)
centre = (resolution[0]//2, resolution[1]//2)
holeRadius = 15
ballRadius = 12

# Fonts
ballFont = pygame.font.SysFont("dubaimedium", int(ballRadius*0.9))
ballUIFont = pygame.font.SysFont("dubaimedium", 18)
fpsFont = pygame.font.SysFont("dubaimedium", 20)
logoFont = pygame.font.Font("Project\other\Orbitron-VariableFont_wght.ttf", 70)
ballPottedFont = pygame.font.Font("Project\other\Orbitron-VariableFont_wght.ttf", 70)

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
    def __init__(self, colour, radius, pos, velocity, mass, number, isStriped): # Constructor Method
        super().__init__()
        self.colour = colour
        self.radius = radius
        self.pos = VEC(pos) # Position Vector
        self.velocity = VEC(velocity) # Velocity vector
        self.mass = mass
        self.number = number # stores the ball number, e.g. the 8 ball
        self.isStriped = isStriped # boolean, stores whether the ball is coloured or striped

    def update(self): # Updates the position of the ball
        self.pos += self.velocity # moves ball to next position
        self.velocity *= friction # reduces the velocity of the ball

        if self.velocity.magnitude_squared() < 0.005:
            self.velocity = VEC(0,0)
        
        # Checking collisions with the outer walls: (ensures all balls stay in region)
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
            # self.pos -= self.velocity # undoes last move, to prevent clipping

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

    def checkHoleCollision(self):
        for i in holePos: # for each hole on the table
            distance2 = self.pos.distance_squared_to(holePos[i]) # compute the distance
            if distance2 <= (holeRadius*0.8)**2: # if colliding
                return True
        return False
                
    def draw(self, screen): # Draws the ball to the screen
        pygame.draw.circle(screen, self.colour, self.pos, self.radius) # draws outer circle
    
        text = ballFont.render(str(self.number),True,"black") # renders font

        pygame.draw.circle(screen, "white", self.pos, text.get_height()/2.2) # draws inner circle
        
        fontPos = [ # offsets the font to be central with ball
            self.pos[0] - text.get_width()/2,
            self.pos[1] - text.get_height()/2
        ]

        screen.blit(text,fontPos) # adds font to screen

        # COMPILE ALL DRAWINGS INTO ONE BLIT

    def delete(self):
        if self.colour != "white": # delete later
            self.kill()

# Slider Class
class Slider(pygame.sprite.Sprite):
    def __init__(self, outerColour, sliderColour, position, width, height, value):
        super().__init__()
        self.outerColour = outerColour # colour of the outer section
        self.sliderColour = sliderColour # colour of the slider
        self.position = position # (x,y)
        self.width = width # width of the slider
        self.height = height # height of the slider
        self.value = value # starting value of the slider
        self.mouseDown = False # for checking if user is interacting with slider
    
    def draw(self, screen): # draw method that draws slider to screen
        # Outer Box
        pygame.draw.rect(
            screen,
            self.outerColour,
            pygame.Rect(
                        self.position[0],
                        self.position[1],
                        self.width,
                        self.height
            ),
            3,
            self.width
        )
        # Slider
        pygame.draw.circle(
            screen,
            self.sliderColour,
            (self.position[0]+self.width/2, self.position[1] + self.value * self.height),
            self.width,
        )

    def update(self): # updates slider position
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # when left mouse button clicked
            mousePos = pygame.mouse.get_pos() # get mouse position
            if 0 <= mousePos[0] - self.position[0] <= self.width: # if click is within x bounds
                if 0 <= mousePos[1] - self.position[1] <= self.height: # if click is within y bounds
                    self.mouseDown = True
        if event.type == pygame.MOUSEBUTTONUP: # when mouse button is released
            self.mouseDown = False
        if self.mouseDown:
            mousePos = pygame.mouse.get_pos() # get mouse position
            distance = mousePos[1]-self.position[1] # finds distance between bottom and mousePos
            self.value = distance/self.height # sets the value of slider to the ratio of distances.
            self.value = max(0, min(1, self.value))
        
    def returnValue(self): # returns slider position value
        return round(1-self.value, 3)


ballPowerSlider = Slider("white", "red", (tableCorners[0][0]/2 - 30,tableCorners[0][1]-30), 30, tableDimensions[1]+60, 0.5) # initialise slider sprite

ballGroup = pygame.sprite.Group() # Groups all balls for easier maintenance

# Ball info
ballInfo = ( # COLOUR, NUMBER, STRIPED
    ("white", 0, False),
    ("yellow", 1, False),
    ("blue", 2, False),
    ("red", 3, False),
    ("purple", 4, False),
    ("orange", 5, False),
    ("green", 6, False),
    ("maroon", 7, False),
    ("black", 8, False),
    ("yellow", 9, True),
    ("blue", 10, True),
    ("red", 11, True),
    ("purple", 12, True),
    ("orange", 13, True),
    ("green", 14, True),
    ("maroon", 15, True),
)

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
    Ball("white", ballRadius, ballStartPos["white0"], (0, 0), 1, 0, False),      # Whiteball
    Ball("yellow", ballRadius, ballStartPos["yellow1"], (0, 0), 1, 1, False),    # Yellow 1
    Ball("blue", ballRadius, ballStartPos["blue2"], (0, 0), 1, 2, False),        # Blue 2
    Ball("red", ballRadius, ballStartPos["red3"], (0, 0), 1, 3, False),          # Red 3
    Ball("purple", ballRadius, ballStartPos["purple4"], (0, 0), 1, 4, False),    # Purple 4
    Ball("orange", ballRadius, ballStartPos["orange5"], (0, 0), 1, 5, False),    # Orange 5
    Ball("green", ballRadius, ballStartPos["green6"], (0, 0), 1, 6, False),      # Green 6
    Ball("maroon", ballRadius, ballStartPos["maroon7"], (0, 0), 1, 7, False),    # Maroon 7
    Ball("black", ballRadius, ballStartPos["black8"], (0, 0), 1, 8, False),      # Black 8
    Ball("yellow", ballRadius, ballStartPos["yellow9"], (0, 0), 1, 9, True),     # Yellow 9
    Ball("blue", ballRadius, ballStartPos["blue10"], (0, 0), 1, 10, True),       # Blue 10
    Ball("red", ballRadius, ballStartPos["red11"], (0, 0), 1, 11, True),         # Red 11
    Ball("purple", ballRadius, ballStartPos["purple12"], (0, 0), 1, 12, True),   # Purple 12
    Ball("orange", ballRadius, ballStartPos["orange13"], (0, 0), 1, 13, True),   # Orange 13
    Ball("green", ballRadius, ballStartPos["green14"], (0, 0), 1, 14, True),     # Green 14
    Ball("maroon", ballRadius, ballStartPos["maroon15"], (0, 0), 1, 15, True),   # Maroon 15
]


for i in balls:
    ballGroup.add(i)

# Pygame Functions
pygame.display.set_caption(borderName)
screen = pygame.display.set_mode(resolution) # Sets up the display
clock = pygame.time.Clock()

# Functions
def checkIfBallMoving(): # Checks if any ball is moving (returns True if any ball is moving)
    ballMoving = False # sets initial case to False
    for ball in ballGroup.sprites():
        if ball.velocity != (0,0): # checks if the ball is completely still
            ballMoving = True # if even one ball is still moving, it is set to True.
    return ballMoving

def distanceToClosestBall(intialPos): # returns distance from closest ball
    closestDistance = float("inf") # sets initial value to infinity
    otherBall = None # sets initial value to none
    for ball in ballGroup.sprites(): # loops through every ball (except whiteball)
        if ball.number != 0: # skip if the ball is itself (white)
            distance = VEC(intialPos).distance_to(ball.pos) # finds the distance between the ball and the whiteball
            if distance < closestDistance: # if the new distance is smaller, set the new distance to the actual distance
                closestDistance = distance
                otherBall = ball
    return closestDistance, otherBall # return the distance and then the instance of the other ball 

def distanceToClosestRail(intialPos): # returns distance from closest rail
    closestDistance = float("inf") # sets initial value to infinity
    railVec = None
    # Loops through each of the Rails (where collisions should be done)
    for i in tableRails:
        for j in range(3):
            lineStart = tableRails[i][j] # Coordinates of the Line Start and End
            lineEnd = tableRails[i][j+1] # e.g. [ [x1,y1] , [x2,y2] ]
            lineVec = VEC(lineEnd[0] - lineStart[0], lineEnd[1] - lineStart[1]) # Vector of the Line
            pointVec = VEC(intialPos[0] - lineStart[0], intialPos[1] - lineStart[1]) # Vector of the circle to the start of the line
            dot = VEC.dot(pointVec,lineVec) # finds the dot product of the vectors
            # This creates a parameter that will calculate the s.f of the normal projection that maps the circle onto the line segment
            t = max(0, min(1, dot / lineVec.magnitude_squared()))
            linePoint = (lineStart[0] + t * lineVec[0], lineStart[1] + t * lineVec[1]) # Calculate closest point on the line to the circle
            circlePointVec = VEC(linePoint[0] - intialPos[0], linePoint[1] - intialPos[1]) # Vector of the circle to the closest point
            distance = circlePointVec.magnitude() # calculates distance between the circle and closest point
            
            # if the new distance is smaller, set the new distance to the actual distance
            if distance < closestDistance: 
                closestDistance = distance
                railVec = lineVec

    return closestDistance, railVec  # returns the distance to the rail and the vector of the rail  


def resolveAllCollisions(): # Checks and resolves every collision between every pair of balls (only if colliding)
    for i in range(len(ballGroup) - 1):
        for j in range(i + 1, len(ballGroup)): # except white ball
            ballGroup.sprites()[i].checkResolveCollision(ballGroup.sprites()[j])

def resolveWallCollisions(): # Checks and resolves every collision between every ball and the walls
    for ball in ballGroup.sprites():
        ball.checkResolveWallCollision() # checks wall collisions

def resolveBallPotted(): # Checks if a ball is potted
    for ball in ballGroup.sprites():
        if ball.checkHoleCollision(): # checks if each ball is in a hole
            ball.delete() # removes the ball from the game
        ball.draw(screen) # draws each ball


def drawTable(): # Draws the table
    
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

def drawBalls(): # Draws all the balls
    for ball in ballGroup.sprites():
        ball.draw(screen)

def drawBallUI(): # Draw 15 balls on screen for UI (NOT ON TABLE)
    increment = 0 # adds a value on each time so the balls are not drawn on top of each other
    distanceBetweenBalls = tableDimensions[0]/(len(ballInfo)-2)
    for i in range(len(ballInfo)-1): # loops through each ball except white ball
        circleCentre = (tableCorners[0][0] + increment, tableCorners[2][1]+75) # coordinates of each circle

        pygame.draw.circle(screen, ballInfo[i+1][0], circleCentre, 25)
        numberFont = ballUIFont.render(str(ballInfo[i+1][1]),True,"black") # renders font
        pygame.draw.circle(screen, "white", circleCentre, numberFont.get_height()/2.2) # draws inner circle
        numberFontPos = [circleCentre[0] - numberFont.get_width()/2,circleCentre[1] - numberFont.get_height()/2]# offsets the font to be central with ball
        screen.blit(numberFont,numberFontPos) # adds font to screen 
        
        potted = True # set inital case to True
        for ball in ballGroup:
            if ball.number == ballInfo[i+1][1]: # If the ball still exists
                potted = False # do not draw X
        if potted: # if ball does not exist on table
            xFont = ballPottedFont.render("X",True,"red") # render font
            xFontPos = [circleCentre[0] - xFont.get_width()/2,circleCentre[1] - xFont.get_height()/2] # centre font
            screen.blit(xFont, xFontPos) # draw ball
        
        increment += distanceBetweenBalls
 
def drawLogo(): # Draws the logo 
    logo = logoFont.render(("BILLIARD CLUB"), True, "white")
    logo = pygame.transform.rotate(logo, 270)
    screen.blit(logo, (resolution[0] - logo.get_width() - 30, centre[1]-logo.get_height()/2))

def drawFPS(): # FPS Display
    currentFPS = str(round(clock.get_fps(), 1))
    text = fpsFont.render((str(currentFPS)), True, "white")
    screen.blit(text, (5, 3))

def drawCue(): # draws the cue
    mousePos = pygame.mouse.get_pos() # get mouse position
    cueVec = (VEC(balls[0].pos) - VEC(mousePos)).normalize() # vector of line
    virtualBallPos = VEC(balls[0].pos) # sets initial position of virtual ball
    
    railDistance, closestRail = distanceToClosestRail(virtualBallPos) # updates distance to closest rail
    ballDistance, closestBall = distanceToClosestBall(virtualBallPos) # updates distance to closest ball

    # rough check for virtual ball collisions
    maxIterations = 1000 # limits the number of iterations the initial while loop will do
    while railDistance > ballRadius and ballDistance > 2*ballRadius and maxIterations > 0 and (
            tableCorners[0][0] + ballRadius <= virtualBallPos[0] <= tableCorners[1][0] - ballRadius\
            and tableCorners[0][1] + ballRadius <= virtualBallPos[1] <= tableCorners[2][1] - ballRadius
    ): # while the ball is not close to a rail (and within the table bounds)
        virtualBallPos += ballRadius*cueVec # get closer to rail
        railDistance, closestRail = distanceToClosestRail(virtualBallPos) # find new distance
        ballDistance, closestBall = distanceToClosestBall(virtualBallPos)
        maxIterations -= 1 # decrement counter
    
    # if ball collides with other ball, set this to true
    collidingWithBall = False
    if ballDistance < 2 * ballRadius:
        collidingWithBall = True
    
    # if ball collides with outer wall first or other ball, don't draw projection.
    drawReflectedProjection = True
    if collidingWithBall or not (tableCorners[0][0] + ballRadius <= virtualBallPos[0] <= tableCorners[1][0] - ballRadius\
            and tableCorners[0][1] + ballRadius <= virtualBallPos[1] <= tableCorners[2][1] - ballRadius):
        drawReflectedProjection = False

    # finer adjustment for virtual ball collisions
    while railDistance < ballRadius or ballDistance < 2*ballRadius or not (
            tableCorners[0][0] + ballRadius <= virtualBallPos[0] <= tableCorners[1][0] - ballRadius\
            and tableCorners[0][1] + ballRadius <= virtualBallPos[1] <= tableCorners[2][1] - ballRadius
    ): # while the ball is colliding with a rail or out of the table bounds
        virtualBallPos -= cueVec # move the ball back by a very small amount
        railDistance, closestRail = distanceToClosestRail(virtualBallPos) # find new distance
        ballDistance, closestBall = distanceToClosestBall(virtualBallPos)

    pygame.draw.line(screen, "red", balls[0].pos, pygame.mouse.get_pos(), 2) # draw cue
    pygame.draw.circle(screen, "white", virtualBallPos, ballRadius, 2) # draw virtual ball
    pygame.draw.line(screen, "white", balls[0].pos, virtualBallPos) # draw projection

    if collidingWithBall:
        virtualBallVec = (virtualBallPos - closestBall.pos).normalize() # vector of virtual ball to other ball
        pygame.draw.circle(screen, "white", closestBall.pos, ballRadius, 3) # draw virtual ball
        pygame.draw.line(screen, "white", closestBall.pos, (closestBall.pos-50*virtualBallVec)) # draw reflected projection
        
    if drawReflectedProjection: # only draw if ball did not collide with outer wall
        reflectedCueVec = VEC(cueVec - 2*(VEC.dot(cueVec, closestRail)/VEC.dot(
            closestRail, closestRail))*closestRail).normalize() # calculated reflected vector projection
        pygame.draw.line(screen, "white", virtualBallPos, (virtualBallPos-50*reflectedCueVec)) # draw reflected projection
    
    if mouseDown: # when clicked
        if tableCorners[0][0] <= mousePos[0] <= tableCorners[1][0] \
            and tableCorners[0][1] <= mousePos[1] <= tableCorners[2][1]: # if mouse is on the pool table
            balls[0].velocity = cueVec*20*ballPowerSlider.returnValue() # give ball a velocity


# Game Loop
while True:
    mouseDown = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Checks if user closes program
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN: # on left click
            mouseDown = True

    ballPowerSlider.update() # Update Slider
    ballGroup.update() # update each ball
    
    resolveAllCollisions() # Checks and resolves every collision between every pair of balls (only if colliding)
    resolveWallCollisions() # Checks and resolves every collision between every ball and the walls
    resolveBallPotted() # checks if a ball is potted and deletes it if it is.
    
    # Draw Everything to Screen:
    
    screen.fill((30, 30, 30)) # Fills the screen with a grey colour
    
    drawTable() # Draws the table
    drawBalls() # draws the balls
    
    if not checkIfBallMoving(): # when all the balls are still
        drawCue() # draw the cue
    
    ballPowerSlider.draw(screen) # Draws slider

    drawBallUI() # draws the ball UI (15 balls that tells the user which ball to pot next)
    drawLogo() # draws the logo
    drawFPS() # draws the FPS

    
    pygame.display.flip() # Updates the display
    clock.tick(FPS) # Caps the frame rate
