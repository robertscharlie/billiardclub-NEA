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

# Pygame Functions and Setup
pygame.display.set_caption(borderName)
screen = pygame.display.set_mode(resolution) # Sets up the display
clock = pygame.time.Clock()

# Table Variables and Setup
primaryTableColour = "#155843"
secondaryTableColour = "#313e46"
outerTableColour = "#313e46"
tableDimensions = (900,450)
centre = (resolution[0]//2, resolution[1]//2)
holeRadius = 15
ballRadius = 12

# Coordinates for the Table Corners.
tableCorners = (
    (centre[0] - tableDimensions[0] / 2, centre[1] - tableDimensions[1] / 2), # Top Left
    (centre[0] + tableDimensions[0] / 2, centre[1] - tableDimensions[1] / 2), # Top Right
    (centre[0] - tableDimensions[0] / 2, centre[1] + tableDimensions[1] / 2), # Bottom Left
    (centre[0] + tableDimensions[0] / 2, centre[1] + tableDimensions[1] / 2), # Bottom Right
)

# Coordinates for Hole Positions
holePos = {
    "TL": (tableCorners[0][0]+1.1*holeRadius, tableCorners[0][1]+1.1*holeRadius), # Top Left
    "TR": (tableCorners[1][0]-1.1*holeRadius, tableCorners[0][1]+1.1*holeRadius), # Top Right
    "BL": (tableCorners[0][0]+1.1*holeRadius, tableCorners[2][1]-1.1*holeRadius), # Bottom Left
    "BR": (tableCorners[1][0]-1.1*holeRadius, tableCorners[2][1]-1.1*holeRadius), # Bottom Right
    "TM": (centre[0], tableCorners[0][1]+1.1*holeRadius), # Top Middle
    "BM": (centre[0], tableCorners[2][1]-1.1*holeRadius), # Bottom Middle
}

# Coordinates for Table Rails
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

# Ball info
ballInfo = ( # COLOUR, NUMBER, STRIPED
    ("white", 0, None),
    ("yellow", 1, False),
    ("blue", 2, False),
    ("red", 3, False),
    ("purple", 4, False),
    ("orange", 5, False),
    ("green", 6, False),
    ("maroon", 7, False),
    ("black", 8, None),
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

# Game Variables
computerPlaying = True # Set to True if you want the computer to play
player1Turn = True # initially player 1's turn
player1BallType = None # Stores the type of balls player 1 is potting
player2BallType = None # Stores the type of balls player 2 is potting
winner = None # Stores the winner of the game
player1Name = "Player 1"
player2Name = "Player 2"
player1Colour = "red"
player2Colour = "blue"

# Fonts
ballFont = pygame.font.SysFont("dubaimedium", int(ballRadius*0.9))
ballUIFont = pygame.font.SysFont("dubaimedium", 18)
fpsFont = pygame.font.SysFont("dubaimedium", 20)
logoFont = pygame.font.Font("Project\other\Orbitron-VariableFont_wght.ttf", 70)
ballPottedFont = pygame.font.Font("Project\other\Orbitron-VariableFont_wght.ttf", 70)
playerIndicatorFont = pygame.font.Font("Project\other\Orbitron-VariableFont_wght.ttf", 60)
MenuLogoFont = pygame.font.Font("Project\other\Orbitron-VariableFont_wght.ttf", 100)

# Classes
class Ball(pygame.sprite.Sprite): # Defines a class for a ball
    def __init__(self, colour, radius, pos, velocity, mass, number, isStriped): # Constructor Method
        super().__init__()
        self.colour = colour
        self.radius = radius
        self.pos = VEC(pos) # Position Vector
        self.velocity = VEC(velocity) # Velocity vector
        self.mass = mass
        self.number = number # stores the ball number, e.g. the 8 ball
        self.isStriped = isStriped # boolean, stores whether the ball is dotted or striped

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
        def checkColliding(self, other):
            posDifference = self.pos - other.pos # find difference in positions
            distance = self.pos.distance_to(other.pos) # distance squared between points
            if distance == 0: # prevents normalisation error
                return False, posDifference
            elif distance < (self.radius + other.radius): # If colliding
                return True, posDifference
            return False, posDifference

        colliding, posDifference = checkColliding(self,other) # checks if colliding
        calculateCollision = False # set initial case to False
        
        if colliding: 
            calculateCollision = True # calculate collision at the end
            self.pos -= self.velocity # step back position of both balls
            other.pos -= other.velocity # step back position of both balls
            colliding, posDifference = checkColliding(self,other) # checks if colliding
            while not colliding: # while colliding
                    # incrementally move the balls forward until they are tangential
                    self.pos += 0.05 * self.velocity 
                    other.pos += 0.05 * other.velocity 
                    colliding, posDifference = checkColliding(self,other) # checks if colliding

        if calculateCollision: # if colliding
            # Calculate Velocities after collision
            n = VEC(posDifference).normalize() # creates a normalised vector as a origin for calculations
            relVel = self.velocity - other.velocity # calculates the relative velocity of the balls
            impulse = 2 * (n * relVel) / (self.mass + other.mass) # calculates the impulse each ball will get
            
            self.velocity -= impulse * other.mass * n # applies impulse to each ball
            other.velocity += impulse * self.mass * n

            self.velocity *= restitutionCoeff # decreases velocity of both balls
            other.velocity *= restitutionCoeff
        
        while colliding: # if still colliding
            # push balls apart to prevent sticking
            self.pos += n
            other.pos -= n
            colliding, posDifference = checkColliding(self,other) # checks if still colliding


    def checkResolveWallCollision(self): # Check if balls are colliding with the walls, then resolves collision
        def checkColliding():
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
                        return True, circlePointVec
            return False, None # if not colliding, return False

        calculateCollision = False  
        isColliding, circlePointVec = checkColliding() # checks if colliding
        
        if isColliding: # if colliding
            calculateCollision = True # calculate collision at the end
            n = circlePointVec.normalize() # creates a normal vector as a origin for calculations

        while isColliding: # while colliding
            self.pos -= self.velocity.normalize()  # incrementally move the ball back until it is no longer colliding
            isColliding, circlePointVec = checkColliding() # checks if colliding

        # Check if colliding
        if calculateCollision:
            impulse = 2*(n*self.velocity)/(self.mass) # calculates the impulse the ball will get
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
    
        if self.isStriped:
            pygame.draw.circle(screen, "white", self.pos, self.radius) # draws outer circle to overlap stripe
            # Draw the stripe
            stripe_height = ballRadius / 0.65 # height of the stripe
            pygame.draw.ellipse(
                screen, 
                self.colour, 
                (
                    self.pos[0] - ballRadius, 
                    self.pos[1] - stripe_height // 2,
                    ballRadius * 2,
                    stripe_height
                )
            )

        text = ballFont.render(str(self.number),True,"black") # renders font
        pygame.draw.circle(screen, "white", self.pos, text.get_height()/2.2) # draws inner circle
        
        fontPos = [self.pos[0] - text.get_width()/2,self.pos[1] - text.get_height()/2] # offsets the font to be central with ball
        
        screen.blit(text,fontPos) # adds font to screen

        # COMPILE ALL DRAWINGS INTO ONE BLIT

    def delete(self):
        self.kill()

class VerticalSlider(pygame.sprite.Sprite): # Vertical Slider Class
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

    def update(self, event): # updates slider position
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

class HorizontalSlider(pygame.sprite.Sprite): # Horizontal Slider Class
    def __init__(self, x, y, width, height, startValue, sliderColour, outerColour, circleColour, sliderType):
        self.sliderType = sliderType
        self.outerColour = outerColour  # Colour of the outer section
        self.sliderColour = sliderColour  # Colour of the slider
        self.x = x  # X position of the slider
        self.y = y  # Y position of the slider
        self.width = width  # Width of the slider
        self.height = height  # Height of the slider
        self.value = startValue  # Starting value of the slider [0,1]
        self.rect = pygame.Rect(x, y, width, height)  # Rectangle representing the slider's position and size
        self.circlePos = [self.x + self.value * self.width, self.y + self.height / 2]  # Calculate the position of the slider circle
        self.clicked = False
        self.circleColour = circleColour
    
    def draw(self):
        pygame.draw.rect(screen, self.outerColour, self.rect, 0, 10)  # Draw the slider rectangle
        if self.sliderType == "colourPicker":  # Check if the slider type is a colour picker
            for i in range(self.width-18):  # Iterate through the width of the slider
                colour = pygame.Color(0)  # Create a new colour object
                colour.hsla = (int(360 * i / self.width), 100, 50, 100)  # Set the colour based on the position
                pygame.draw.rect(screen, colour, (self.x+i, self.y, self.width - i, self.height), 0, 10)  # Draw the colour rectangle
        else:
            pygame.draw.rect(screen, self.sliderColour, (self.x, self.y, self.width*self.value, self.height), 0, 10)  # Draw the colour rectangle
        pygame.draw.rect(screen, self.outerColour, self.rect, 1, 10)  # Draw the outer slider rectangle
        pygame.draw.circle(screen, self.outerColour, self.circlePos, self.height * 0.6 + 1)  # Draw outer circle
        if self.sliderType == "colourPicker":
            pygame.draw.circle(screen, self.getColour(), self.circlePos, self.height * 0.6)  # Draw the slider circle
        else:
            pygame.draw.circle(screen, self.circleColour, self.circlePos, self.height * 0.6)  # Draw the slider circle
        
    def getColour(self):
        # calculate selected Colour
        selectedColour = pygame.Color(0)
        selectedColour.hsla = (int(self.value * (self.width+60)), 100, 50, 100) 
        return selectedColour

    def returnValue(self):
        self.value = (self.circlePos[0]-self.x)/self.width # update value (between 0 and 1)
        return self.value


    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check if the left mouse button is clicked
            if self.rect.collidepoint(event.pos):  # Check if the text box was clicked
                self.clicked = True
            else:
                self.clicked = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # When mouse button is released
            self.clicked = False
    
    def update(self):
        if self.clicked: # when clicked
            mousePos = pygame.mouse.get_pos() # get mouse position
            self.circlePos[0] = min(max(self.x, mousePos[0]), self.x + self.width) # update position
            self.value = (self.circlePos[0]-self.x)/self.width # update value (between 0 and 1)

class Button:  # Defines Button class
    def __init__(self, text, fontSize, x, y, padding, callback):
        self.text = text  # Text to display on the button
        self.font = pygame.font.Font("C:/Users/crobe/Documents/GitHub/billiardclub-NEA/Project/other/Orbitron-VariableFont_wght.ttf", fontSize)  # Font for the button text
        self.callback = callback  # Function to call when the button is clicked
        
        self.hovering = False # Set to true if the mouse is hovering over.
        self.wasClicked = False

        self.boxColour = "white"  # Button colour
        self.boxColourClicked = "grey" # Button colour when clicked
        self.textColour = "black" # Text colour when the mouse is not hovering over
        self.textColourHovering = "red" # Text colour when the mouse is hovering over

        self.textSurface = self.font.render(self.text, True, self.textColour) # Render the button text
        # Rectangle representing the button's position and size
        self.rect = pygame.Rect(x, y, self.textSurface.get_width() + padding, self.textSurface.get_height() + padding,)

    def draw(self):
        textColour = ""
        boxColour = ""
        if self.hovering:  # Check if the button is being hovered over
            textColour = self.textColourHovering  # Set textColour to hovering colour
        else:
            textColour = self.textColour  # Set textColour to default colour
        if self.wasClicked:  # Check if the button is clicked
            boxColour = self.boxColourClicked  # Set boxColour to clicked colour
        else:
            boxColour = self.boxColour  # Set boxColour to default colour
        self.textSurface = self.font.render(self.text, True, textColour) # Render the button text 
        pygame.draw.rect(screen, boxColour, self.rect, 0, 10) # Draw the button rectangle
        textRect = self.textSurface.get_rect(center=self.rect.center) # Get the rectangle for the text surface
        screen.blit(self.textSurface, textRect) # Draw the text on the button

    def checkHover(self, mousePos):  # checks if the mouse is over the button.
        if self.rect.collidepoint(mousePos):  # Check if the mouse position is within the button rectangle
            self.hovering = True # Sets to True if hovering
            return True # returns true to say the mouse is hovering over
        else:
            self.hovering = False # Sets to False if hovering
            return False # returns False to say the mouse is hovering over

class Menu:  # Defines Menu class
    def __init__(self, fontSize, pos, options, functions):  # Initializes the Menu class
        self.fontSize = fontSize  # Font size for the menu options
        self.pos = pos  # Position of the menu
        self.options = options  # List of menu options
        self.functions = functions  # List of functions corresponding to each menu option
        self.buttons = []  # List to store buttons
        self.create_buttons()  # Calls the method to create buttons

    def create_buttons(self):  # Method to create buttons

        increment = (resolution[1]-200)/(len(self.options)-1)  # Vertical spacing between buttons
        
        for i in range(len(self.options)):  # Iterate through the options
            # Create a button for each option and append it to the buttons list along with its function when clicked
            self.buttons.append(Button(self.options[i], self.fontSize, self.pos[0], self.pos[1] + i*increment, 20, self.functions[i]))

    def draw(self):  # Method to draw buttons
        for button in self.buttons:  # Iterate through each button
            button.draw()  # Draw the button

    def update(self):  # Method to update button states
        for button in self.buttons:  # Iterate through each button
            button.checkHover(pygame.mouse.get_pos())  # Check if the mouse is hovering over the button
    
    def handleEvent(self, event):  # Method to handle events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check if the left mouse button is clicked
            for button in self.buttons:  # Iterate through each button
                if button.checkHover(event.pos):  # Check if click occurred and if hovering over button
                    button.wasClicked = True  # Set button as clicked
                else:
                    button.wasClicked = False  # Set button as not clicked
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # When mouse button is released
            for button in self.buttons:  # Iterate through each button
                if button.wasClicked:
                    button.wasClicked = False
                    eval(button.callback)  # Execute the button's callback function
                button.wasClicked = False  # Set button as not clicked

class TextBox:  # Defines TextBox class
    def __init__(self, x, y, permanentText, initialText, fontSize):  # Initializes the TextBox class
        self.permanentText = permanentText # permanent Text that can't be deleted by user in the text field
        self.text = initialText  # Initial text to display in the text box
        self.font = pygame.font.Font("Project/other/Orbitron-VariableFont_wght.ttf", fontSize)  # Font for the text box text
        self.textColour = "black"  # Text colour
        self.boxColour = "white"  # Box colour
        self.active = False  # Indicates if the text box is active (clicked)
        # Colours for the text box when active and passive
        self.colourActive = "red"
        self.colourPassive = "black"
        self.textSurface = self.font.render(permanentText + self.text, True, self.textColour)  # Render the text
        # Rectangle representing the text box's position and size
        self.rect = pygame.Rect(x, y, self.textSurface.get_width() + 10, self.textSurface.get_height() + 10)
    
    def draw(self):  # Method to draw the text box
        if self.active:  # Check if the text box is active
            self.textColour = self.colourActive  # Set text colour to active colour
        else:
            self.textColour = self.colourPassive  # Set text colour to passive colour

        self.rect.w = self.textSurface.get_width() + 10  # Update the width of the text box rectangle based on the text width

        self.textSurface = self.font.render(self.permanentText + self.text, True, self.textColour)  # Render the text
        pygame.draw.rect(screen, self.boxColour, self.rect, 0, 10)  # Draw the text box rectangle
        textRect = self.textSurface.get_rect(center=self.rect.center)  # Get the rectangle for the text surface
        screen.blit(self.textSurface, textRect)  # Draw the text on the text box

    def handle_event(self, event):  # Method to handle events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check if the left mouse button is clicked
            if self.rect.collidepoint(event.pos):  # Check if the text box was clicked
                self.active = True  # Set text box as active
            else:
                self.active = False  # Set text box as inactive
        if event.type == pygame.KEYDOWN:  # Check if a key is pressed
            if self.active:  # Check if the text box is active
                if event.key == pygame.K_RETURN:  # Check if the Enter key is pressed
                    self.active = False  # Set text box as inactive
                elif event.key == pygame.K_BACKSPACE:  # Check if the Backspace key is pressed
                    self.text = self.text[:-1]  # Remove the last character
                else:
                    self.text += event.unicode  # Add the character to the text
                self.textSurface = self.font.render(self.permanentText + self.text, True, self.textColour)  # Re-render the text

# Initialise Menus
mainMenu = Menu(60, [50,50], ["Start", "Options", "Quit"], ["gameModeScreen()", "optionsScreen()", "quitGame()"]) # create a menu
gameModeMenu = Menu(60, [50,50], ["Player vs Player", "Player vs AI", "Sandbox Mode", "Back"], ["runGame(False, False)", "runGame(True, False)", "runGame(False, True)", "mainMenuScreen()"]) # create a menu
optionsMenu = Menu(60, [50,50], ["Customise Game", "Volume Control", "Back"], ["customisationScreen()", "volumeControlScreen()", "mainMenuScreen()"]) # create a menu
customisationMenu = Menu(60, [50,50], ["Customise Game", "Back"], ["customisationScreen()", "optionsScreen()"]) # create a menu
pauseMenu = Menu(60, [50,50], ["Game Paused", "Exit Game"], ["print()", "mainMenuScreen()"]) # create a menu
volumeMenu = Menu(60, [50,50], ["Volume Control", "Back"], ["volumeControlScreen()", "optionsScreen()"]) # create a menu
# Initialise Slider sprite
ballPowerSlider = VerticalSlider("white", "red", (tableCorners[0][0]/2 - 30,tableCorners[0][1]-30), 30, tableDimensions[1] + 60, 0.5) 

# Initialise each ball
balls = [
    Ball("white", ballRadius, ballStartPos["white0"], (0, 0), 1, 0, None),      # Whiteball
    Ball("yellow", ballRadius, ballStartPos["yellow1"], (0, 0), 1, 1, False),    # Yellow 1
    Ball("blue", ballRadius, ballStartPos["blue2"], (0, 0), 1, 2, False),        # Blue 2
    Ball("red", ballRadius, ballStartPos["red3"], (0, 0), 1, 3, False),          # Red 3
    Ball("purple", ballRadius, ballStartPos["purple4"], (0, 0), 1, 4, False),    # Purple 4
    Ball("orange", ballRadius, ballStartPos["orange5"], (0, 0), 1, 5, False),    # Orange 5
    Ball("green", ballRadius, ballStartPos["green6"], (0, 0), 1, 6, False),      # Green 6
    Ball("maroon", ballRadius, ballStartPos["maroon7"], (0, 0), 1, 7, False),    # Maroon 7
    Ball("black", ballRadius, ballStartPos["black8"], (0, 0), 1, 8, None),      # Black 8
    Ball("yellow", ballRadius, ballStartPos["yellow9"], (0, 0), 1, 9, True),     # Yellow 9
    Ball("blue", ballRadius, ballStartPos["blue10"], (0, 0), 1, 10, True),       # Blue 10
    Ball("red", ballRadius, ballStartPos["red11"], (0, 0), 1, 11, True),         # Red 11
    Ball("purple", ballRadius, ballStartPos["purple12"], (0, 0), 1, 12, True),   # Purple 12
    Ball("orange", ballRadius, ballStartPos["orange13"], (0, 0), 1, 13, True),   # Orange 13
    Ball("green", ballRadius, ballStartPos["green14"], (0, 0), 1, 14, True),     # Green 14
    Ball("maroon", ballRadius, ballStartPos["maroon15"], (0, 0), 1, 15, True),   # Maroon 15
]

ballGroup = pygame.sprite.Group() # Groups all balls for easier maintenance

for i in balls: # adds each ball to the group
    ballGroup.add(i)

# Game Functions
def checkIfBallMoving(): # Checks if any ball is moving (returns True if any ball is moving)
    ballMoving = False # sets initial case to False
    for ball in ballGroup.sprites():
        if ball.velocity != (0,0): # checks if the ball is completely still
            ballMoving = True # if even one ball is still moving, it is set to True.
    return ballMoving

def distanceToClosestBall(intialPos, type): # returns distance from closest ball
    closestDistance = float("inf") # sets initial value to infinity
    otherBall = None # sets initial value to none
    for ball in ballGroup.sprites(): # loops through every ball (except whiteball)
        if  (type == "striped" and ball.isStriped and not ball.number == 8) or \
            (type == "dotted" and not ball.isStriped and not ball.number == 8) or \
            (type == None): # if the ball is the specified type or not classified
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
        for j in range(i, len(ballGroup)):
            ballGroup.sprites()[i].checkResolveCollision(ballGroup.sprites()[j])

def resolveWallCollisions(): # Checks and resolves every collision between every ball and the walls
    for ball in ballGroup.sprites():
        ball.checkResolveWallCollision() # checks wall collisions

def resolveBallPotted(): # Checks if a ball is potted
    for ball in ballGroup.sprites():
        if ball.checkHoleCollision(): # checks if each ball is in a hole
            if ball.number == 0: # if the white ball is potted
                gameQueue.append(resetWhiteBall) # tells the game to reset the white ball on the start of the round
                balls[0].velocity = VEC(0,0) # resets the velocity of the white ball
                balls[0].pos = VEC(0,0) # resets the position of the white ball

            else:
                # On first run, set the ball type for each player
                global player1BallType, player2BallType
                if player1BallType == None and player2BallType == None: 
                    if ball.isStriped and player1Turn or not ball.isStriped and not player1Turn:
                        player1BallType = "striped"
                        player2BallType = "dotted"
                    elif ball.isStriped and not player1Turn or not ball.isStriped and player1Turn:
                        player1BallType = "dotted"
                        player2BallType = "striped"
                    else:
                        print("Error: Ball type not set")
                    
                pottedBallInfo = [ball.number, ball.isStriped] # collects information about the potted ball

                pottedBalls.append(pottedBallInfo) # adds the ball number to the list of potted balls
                roundPottedBalls.append(pottedBallInfo) # adds the ball number to the list of the round's potted balls

                ball.delete() # removes the ball from the game
        
        ball.draw(screen) # draws each ball

def resetWhiteBall(): # resets the white ball
    balls[0].pos = ballStartPos["white0"] # resets the position of the white ball

def gameLogic(): # determines state of next round on all factors
    global player1Turn
    global player1BallType
    global player2BallType
    global pottedBalls
    global roundPottedBalls
    global gameQueue
    global winner

    changeTurn = False # set initial case to False
    eightBallPotted = False # set initial case to False

    if len(roundPottedBalls) == 0: # if no balls are potted
        changeTurn = True # switch turns
    else:
        for i in roundPottedBalls: # loop through each ball potted
            number = i[0]
            isStriped = i[1]
    
            if number == 8: # if the 8 ball is potted
                eightBallPotted = True # set case to True

            if number == 0: # if the white ball is potted
                changeTurn = True

            if player1Turn: # if it is player 1's turn
                if player1BallType == "dotted": # if player 1 type is dotted
                    if isStriped: # if the ball is striped
                        changeTurn = True
                elif player1BallType == "striped": # if player 1 type is striped
                    if not isStriped: # if the ball is dotted
                        changeTurn = True
            if not player1Turn: # if it is player 2's turn
                if player2BallType == "dotted": # if player 2 type is dotted
                    if isStriped: # if the ball is striped
                        changeTurn = True
                elif player2BallType == "striped": # if player 2 type is striped
                    if not isStriped: # if the ball is dotted
                        changeTurn = True

    if eightBallPotted: # if the 8 ball is potted
        # check if all other balls are potted.
        dottedPotted = 0
        stripedPotted = 0
        # count the number of potted balls from each type
        for i in pottedBalls: 
            if i[1]:
                stripedPotted += 1
            else:
                dottedPotted += 1
        
        if dottedPotted == 7 or stripedPotted == 7:
            # whoever potted the 8 ball wins
            if player1Turn:
                winner = player1Name
            else:
                winner = player2Name
        else:
            # whoever potted the 8 ball loses
            if player1Turn:
                winner = player2Name
            else:
                winner = player1Name
                
    if changeTurn: # if the turn is to be changed
        player1Turn = not player1Turn # switch turns
    
    roundPottedBalls = [] # resets the list of potted balls

def checkWin(winner): # checks if there is a winner
    if winner != None: # if there is a winner
        winText = logoFont.render(winner + " wins!",True,"white") # renders the font
        winTextPos = [centre[0] - winText.get_width()/2, centre[1] - winText.get_height()/2] # offsets the font to be central
        screen.blit(winText,winTextPos) # adds font to screen   

def computerShoot(): # computer finds shot and takes shot
    global player2BallType

    if player2BallType == None: # if the ball type is not set
        # find closest ball and hit it
        distance, closestBall = distanceToClosestBall(balls[0].pos, type=None) # find closest ball
        ballVec = (closestBall.pos - balls[0].pos).normalize() # vector of the ball to the white ball
        balls[0].velocity = ballVec*20 # give ball a velocity

    else:
        # find closest ball of that ball type and hit it

        hitEightBall = True # set initial case to True
        for i in ballGroup.sprites(): # loop through each ball
            if i.number == 8 or i.number == 0: # if the ball is the 8 ball or the white ball
                continue # skip the ball
            elif (player2BallType == "striped" and i.isStriped) or (player2BallType == "dotted" and not i.isStriped): # if there is a ball of correct type, hit that ball
                hitEightBall = False # set case to False
            else: 
                print("no ball of correct type to hit") # if there is no ball of correct type, return error

        if hitEightBall: # if there is no ball of correct type, hit the 8 ball
            ballVec = (balls[8].pos - balls[0].pos).normalize() # vector of the ball to the white ball
            balls[0].velocity = ballVec*20 # give ball a velocity
        else:
            distance, closestBall = distanceToClosestBall(balls[0].pos, type=player2BallType) # find closest ball of correct type
            ballVec = (closestBall.pos - balls[0].pos).normalize() # vector of the ball to the white ball
            balls[0].velocity = ballVec*20 # give ball a velocity
 
def drawMenuLogo():
    # Render the menu logo text
    menuLogo1 = MenuLogoFont.render(("BILLIARD"), True, "white")
    menuLogo2 = MenuLogoFont.render(("CLUB"), True, "white")
    menuLogo1OUTLINE = MenuLogoFont.render(("BILLIARD"), True, "black")
    menuLogo2OUTLINE = MenuLogoFont.render(("CLUB"), True, "black")

    # Calculate the position for the logos
    logoPos = (centre[0] + 300, centre[1])
    logo1Pos = (logoPos[0] - menuLogo1.get_width() // 2, logoPos[1] - menuLogo1.get_height())
    logo2Pos = (logoPos[0] - menuLogo2.get_width() // 2, logoPos[1])

    # Draw the outline of the logo
    for i in range(-4,5):
            for j in range(-4,5):
                screen.blit(menuLogo1OUTLINE, (logo1Pos[0]+i,logo1Pos[1]+j))
                screen.blit(menuLogo2OUTLINE, (logo2Pos[0]+i,logo2Pos[1]+j))

    # Draw the logos on the screen
    screen.blit(menuLogo1, logo1Pos)
    screen.blit(menuLogo2, logo2Pos)

def quitGame(): # Function to quit the game
    pygame.quit()
    exit()
  
# Draw Elements to Screen
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

def drawBallUI(isSandbox): # Draw 15 balls on screen for UI (NOT ON TABLE)
    increment = 0 # adds a value on each time so the balls are not drawn on top of each other
    distanceBetweenBalls = tableDimensions[0]/(len(ballInfo)-2)
    largerBallRadius = 25

    for i in range(len(ballInfo)-1): # loops through each ball except white ball
        circleCentre = (tableCorners[0][0] + increment, tableCorners[2][1]+75) # coordinates of each circle

        pygame.draw.circle(screen, ballInfo[i+1][0], circleCentre, largerBallRadius) # draws outer circle

        if ballInfo[i+1][2]:
            pygame.draw.circle(screen, "white", circleCentre, largerBallRadius) # draws outer circle to overlap stripe
            # Draw the stripe
            stripe_height = largerBallRadius / 0.65 # height of the stripe
            pygame.draw.ellipse(
                screen, 
                ballInfo[i+1][0], 
                (
                    circleCentre[0] - largerBallRadius, 
                    circleCentre[1] - stripe_height // 2,
                    largerBallRadius * 2,
                    stripe_height
                )
            )

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

    if not isSandbox: # don't draw this if in sandbox mode
        line1start = (tableCorners[0][0] - largerBallRadius, circleCentre[1] - largerBallRadius - 10)
        line1end = (centre[0] - distanceBetweenBalls + largerBallRadius, circleCentre[1] - largerBallRadius - 10)

        line2start = (tableCorners[3][0] + largerBallRadius, circleCentre[1] - largerBallRadius - 10)
        line2end = (centre[0] + distanceBetweenBalls - largerBallRadius, circleCentre[1] - largerBallRadius - 10)

        line3start = (tableCorners[0][0] - largerBallRadius, circleCentre[1] + largerBallRadius + 10)
        line3end = (centre[0] - distanceBetweenBalls + largerBallRadius, circleCentre[1] + largerBallRadius + 10)

        line4start = (tableCorners[3][0] + largerBallRadius, circleCentre[1] + largerBallRadius + 10)
        line4end = (centre[0] + distanceBetweenBalls - largerBallRadius, circleCentre[1] + largerBallRadius + 10)

        if player1BallType == "dotted":
            pygame.draw.line(screen, player1Colour, line1start, line1end, 5) # draw lines of player 1
            pygame.draw.line(screen, player1Colour, line3start, line3end, 5) # draw lines of player 1
            pygame.draw.line(screen, player2Colour, line2start, line2end, 5) # draw line of player 2
            pygame.draw.line(screen, player2Colour, line4start, line4end, 5) # draw line of player 2
        elif player1BallType == "striped":
            pygame.draw.line(screen, player2Colour, line1start, line1end, 5) # draw lines of player 2
            pygame.draw.line(screen, player2Colour, line3start, line3end, 5) # draw lines of player 2
            pygame.draw.line(screen, player1Colour, line2start, line2end, 5) # draw line of player 1
            pygame.draw.line(screen, player1Colour, line4start, line4end, 5) # draw line of player 1

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
    ballDistance, closestBall = distanceToClosestBall(virtualBallPos, type=None) # updates distance to closest ball

    # rough check for virtual ball collisions
    maxIterations = 1000 # limits the number of iterations the initial while loop will do
    while railDistance > ballRadius and ballDistance > 2*ballRadius and maxIterations > 0 and (
            tableCorners[0][0] + ballRadius <= virtualBallPos[0] <= tableCorners[1][0] - ballRadius\
            and tableCorners[0][1] + ballRadius <= virtualBallPos[1] <= tableCorners[2][1] - ballRadius
    ): # while the ball is not close to a rail (and within the table bounds)
        virtualBallPos += ballRadius*cueVec # get closer to rail
        railDistance, closestRail = distanceToClosestRail(virtualBallPos) # find new distance
        ballDistance, closestBall = distanceToClosestBall(virtualBallPos, type=None)
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
        ballDistance, closestBall = distanceToClosestBall(virtualBallPos, type=None)

    cueColour = "" # set colour of cue
    if player1Turn:
        cueColour = player1Colour
    else:
        cueColour = player2Colour

    virtualBallColour = "white" # set colour of virtual ball
    if collidingWithBall:

        if closestBall.number == 8: # if the ball is the 8 ball
            virtualBallColour = "red" # set colour to black

        if player1Turn: # if it is player 1's turn
            if player1BallType == "dotted": # if player 1 type is dotted
                if closestBall.isStriped: # if the ball is striped
                    virtualBallColour = "red" # set colour to red
            elif player1BallType == "striped": # if player 1 type is striped
                if not closestBall.isStriped: # if the ball is dotted
                    virtualBallColour = "red" # set colour to red
        if not player1Turn: # if it is player 2's turn
            if player2BallType == "dotted": # if player 2 type is dotted
                if closestBall.isStriped: # if the ball is striped
                    virtualBallColour = "red" # set colour to red
            elif player2BallType == "striped": # if player 2 type is striped
                if not closestBall.isStriped: # if the ball is dotted
                    virtualBallColour = "red" # set colour to red

    pygame.draw.line(screen, cueColour, balls[0].pos, pygame.mouse.get_pos(), 2) # draw cue
    pygame.draw.circle(screen, virtualBallColour, virtualBallPos, ballRadius, 2) # draw virtual ball
    pygame.draw.line(screen, "white", balls[0].pos, virtualBallPos) # draw projection

    if collidingWithBall:
        virtualBallVec = (virtualBallPos - closestBall.pos).normalize() # vector of virtual ball to other ball
        pygame.draw.circle(screen, virtualBallColour, closestBall.pos, ballRadius, 3) # draw virtual ball
        pygame.draw.line(screen, virtualBallColour, closestBall.pos, (closestBall.pos-50*virtualBallVec)) # draw reflected projection
        
    if drawReflectedProjection: # only draw if ball did not collide with outer wall
        reflectedCueVec = VEC(cueVec - 2*(VEC.dot(cueVec, closestRail)/VEC.dot(
            closestRail, closestRail))*closestRail).normalize() # calculated reflected vector projection
        pygame.draw.line(screen, virtualBallColour, virtualBallPos, (virtualBallPos-50*reflectedCueVec)) # draw reflected projection

    if mouseDown: # when clicked
        if tableCorners[0][0] <= mousePos[0] <= tableCorners[1][0] \
            and tableCorners[0][1] <= mousePos[1] <= tableCorners[2][1]: # if mouse is on the pool table
            balls[0].velocity = cueVec*20*ballPowerSlider.returnValue() # give ball a velocity

def drawPlayerIndicator(): # Draws the player indicator
    # render font
    player1Text = playerIndicatorFont.render((player1Name), True, player1Colour)
    vsText = playerIndicatorFont.render(("vs"), True, "white")
    player2Text = playerIndicatorFont.render((player2Name), True, player2Colour)
    
    player1arrowText = playerIndicatorFont.render(("=>"), True, "white")
    player2arrowText = playerIndicatorFont.render(("<="), True, "white")

    # draw font to screen
    screen.blit(player1Text, (centre[0] - player1Text.get_width() - vsText.get_width(), 10))
    screen.blit(vsText, (centre[0] - vsText.get_width()/2, 10))
    screen.blit(player2Text, (centre[0] + vsText.get_width(), 10))

    if player1Turn:
        screen.blit(player1arrowText, (centre[0] - player1Text.get_width() - vsText.get_width() - player1arrowText.get_width()*1.5, 10))
    else:
        screen.blit(player2arrowText, (centre[0] + player2Text.get_width() + vsText.get_width() + player2arrowText.get_width()/2, 10))

# Screens
def mainMenuScreen(): # Main loop for the main menu
    running = True
    while running:
        for menuEvent in pygame.event.get():  # Iterate through the events
            if menuEvent.type == pygame.QUIT:  # Check if the quit event is triggered
                running = False  # Exit the loop
            mainMenu.handleEvent(menuEvent)  # Check if any button is clicked
            
        screen.fill((30, 30, 30))  # Fills the screen with a grey colour
        drawTable()  # Draws the table on the screen
        drawBalls()  # Draws the balls on the screen
        drawMenuLogo()  # Draws the menu logo on the screen

        mainMenu.draw()  # Draw the menu
        mainMenu.update()  # Update the menu
        pygame.display.flip()  # Update the display

def gameModeScreen(): # Main loop for the game mode selection screen
    running = True
    while running:
        for menuEvent in pygame.event.get():  # Iterate through the events
            if menuEvent.type == pygame.QUIT:  # Check if the quit event is triggered
                running = False  # Exit the loop
            gameModeMenu.handleEvent(menuEvent)  # Check if any button is clicked    
        
        screen.fill((30, 30, 30)) # Fills the screen with a grey colour
        drawTable()
        drawBalls()
        drawMenuLogo()
        gameModeMenu.draw()  # Draw the menu
        gameModeMenu.update()  # Update the menu
        pygame.display.flip()  # Update the display

def optionsScreen(): # Main loop for the options screen
    running = True
    while running:
        for menuEvent in pygame.event.get():  # Iterate through the events
            if menuEvent.type == pygame.QUIT:  # Check if the quit event is triggered
                running = False  # Exit the loop
            optionsMenu.handleEvent(menuEvent)  # Check if any button is clicked    
        
        screen.fill((30, 30, 30)) # Fills the screen with a grey colour
        drawTable()
        drawBalls()
        drawMenuLogo()
        
        optionsMenu.draw()  # Draw the menu
        optionsMenu.update()  # Update the menu
        pygame.display.flip()  # Update the display

def customisationScreen(): # Main loop for the customisation screen
    global player1Name
    global player2Name
    global player1Colour
    global player2Colour

    if player2Name == "Computer":
        player2Name == "Player 2"

    TextBox1 = TextBox(70, 175, "Player 1 Name: ", player1Name, 30)
    TextBox3 = TextBox(70, 250, "Player 1 Colour: ", "", 30)
    TextBox2 = TextBox(70, 325, "Player 2 Name: ", player2Name, 30)
    TextBox4 = TextBox(70, 400, "Player 2 Colour: ", "", 30)
    colourSlider1 = HorizontalSlider(390, 265, 260, 20, 0, "orange", "black", "white", "colourPicker")
    colourSlider2 = HorizontalSlider(390, 415, 260, 20, 0.7, "orange", "black", "white", "colourPicker")

    running = True
    while running:
        for menuEvent in pygame.event.get():  # Iterate through the events
            if menuEvent.type == pygame.QUIT:  # Check if the quit event is triggered
                running = False  # Exit the loop
            customisationMenu.handleEvent(menuEvent)  # Check if any button is clicked    
            TextBox1.handle_event(menuEvent)
            TextBox2.handle_event(menuEvent)
            colourSlider1.handleEvent(menuEvent)
            colourSlider2.handleEvent(menuEvent)
        
        screen.fill((30, 30, 30)) # Fills the screen with a grey colour
        drawTable()
        drawBalls()
        drawMenuLogo()
        
        customisationMenu.draw()  # Draw the menu
        customisationMenu.update()  # Update the menu

        TextBox1.draw()  # Draw the first text box
        TextBox2.draw()  # Draw the second text box

        # Not interactive Text boxes
        TextBox3.draw()  # Draw the first text box
        TextBox4.draw()  # Draw the second text box

        player1Name = TextBox1.text  # Update player 1 name with the text from the first text box
        player2Name = TextBox2.text  # Update player 2 name with the text from the second text box

        colourSlider1.update()
        colourSlider1.draw()

        colourSlider2.update()
        colourSlider2.draw()

        player1Colour = colourSlider1.getColour()
        player2Colour = colourSlider2.getColour()



        pygame.display.flip()  # Update the display

def pauseScreen(): # Main loop for the pause screen
    running = True    
    while running:
        for event in pygame.event.get():  # Iterate through the events
            if event.type == pygame.QUIT:  # Check if the quit event is triggered
                running = False  # Exit the loop
            if event.type == pygame.KEYDOWN:  # Check if a key is released
                if event.key == pygame.K_ESCAPE:  # Check if the key is ESCAPE
                    running = False  # Exit the loop
            pauseMenu.handleEvent(event)

        screen.fill((30, 30, 30))  # Fills the screen with a grey colour
        drawTable()  # Draw the table
        drawBalls()  # Draw the balls
        drawMenuLogo() # Draw the Logo for the menu screen

        pauseMenu.draw() # draw the menu
        pauseMenu.update()  # Update the menu
        pygame.display.flip()  # Update the display
 
def volumeControlScreen(): # Main loop for the volume control screen
    
    # Initialise Sliders
    masterVolumeSlider = HorizontalSlider(390, 245, 260, 20, 1, "green", (30, 30, 30), "white", "normal")
    musicVolumeSlider = HorizontalSlider(390, 345, 260, 20, 1, "green", (30, 30, 30), "white", "normal")
    ballVolumeSlider = HorizontalSlider(390, 445, 260, 20, 1, "green", (30, 30, 30), "white", "normal")
    
    # Initialise Text Boxes
    TextBox1 = TextBox(70, 230, "Master Volume", "", 30)
    TextBox2 = TextBox(70, 330, "Music Volume", "", 30)
    TextBox3 = TextBox(70, 430, "Ball Sounds", "", 30)


    running = True    
    while running:
        for event in pygame.event.get():  # Iterate through the events
            if event.type == pygame.QUIT:  # Check if the quit event is triggered
                running = False  # Exit the loop
            
            volumeMenu.handleEvent(event)
            masterVolumeSlider.handleEvent(event)
            musicVolumeSlider.handleEvent(event)
            ballVolumeSlider.handleEvent(event)
            

        screen.fill((30, 30, 30))  # Fills the screen with a grey colour
        drawTable()  # Draw the table
        drawBalls()  # Draw the balls
        drawMenuLogo() # Draw the Logo for the menu screen

        masterVolumeSlider.update()  # Update master volume slider
        masterVolumeSlider.draw()  # Draw master volume slider

        musicVolumeSlider.update()  # Update music volume slider
        musicVolumeSlider.draw()  # Draw music volume slider

        ballVolumeSlider.update()  # Update ball volume slider
        ballVolumeSlider.draw()  # Draw ball volume slider

        TextBox1.draw()  # Draw the Master Volume text box
        TextBox2.draw()  # Draw the Music Volume text box
        TextBox3.draw()  # Draw the Ball sounds text box

        volumeMenu.draw() # draw the menu
        volumeMenu.update()  # Update the menu

        pygame.display.flip()  # Update the display

# Run game
def runGame(computerPlaying, sandbox): # Function to start a new game
    newGame(computerPlaying, sandbox, player1Name, player2Name, player1Colour, player2Colour)
  
def newGame(computerPlaying, sandbox, player1Nametemp, player2Nametemp, player1Colourtemp, player2Colourtemp):
    global gameQueue
    global pottedBalls
    global roundPottedBalls
    global mouseDown

    global player1Name
    global player2Name
    global player1Colour
    global player2Colour


    player1Name = player1Nametemp
    player2Name = player2Nametemp
    player1Colour = player1Colourtemp
    player2Colour = player2Colourtemp


    if computerPlaying:
        player2Name = "Computer"

    gameQueue = [] # Queue/List for storing events in between each turn.
    pottedBalls = [] # List for storing potted balls in whole game
    roundPottedBalls = [] # List for storing potted balls in each round

    # Game Loop
    while True:
        mouseDown = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Checks if user closes program
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN: # on left click
                mouseDown = True

            if event.type == pygame.KEYDOWN:# Check if any key is pressed
                if event.key == pygame.K_ESCAPE: # Check if the key is ESCAPE
                    pauseScreen() # Call the pause screen function

            ballPowerSlider.update(event) # Update Slider
        ballGroup.update() # update each ball
        
        resolveAllCollisions() # Checks and resolves every collision between every pair of balls (only if colliding)
        resolveWallCollisions() # Checks and resolves every collision between every ball and the walls
        resolveBallPotted() # checks if a ball is potted and deletes it if it is.


        # Draw Everything to Screen:
        
        screen.fill((30, 30, 30)) # Fills the screen with a grey colour
        
        drawTable() # Draws the table
        drawBalls() # draws the balls

        if not checkIfBallMoving(): # when all the balls are still
            # execute all functions/procedures in the queue
            for function in gameQueue:
                function() # execute the event
            gameQueue.clear() # clear the queue

            if computerPlaying and not player1Turn: # if computer is playing
                computerShoot() # computer finds shot and takes shot
            else: # if computer is not playing
                drawCue() # draw the cue and give velocity to the white ball if clicked

            # if the ball has been hit 
            if checkIfBallMoving() and not sandbox:
                gameQueue.append(gameLogic) # when the balls are next still, apply game logic to determine the next round.

        ballPowerSlider.draw(screen) # Draws slider

        drawBallUI(sandbox) # draws the ball UI (15 balls that tells the user which ball to pot next)
        drawLogo() # draws the logo
        drawFPS() # draws the FPS
        
        if not sandbox:
            drawPlayerIndicator() # draws the player indicator
            checkWin(winner) # checks if there is a winner and draws it to the screen

        pygame.display.flip() # Updates the display
        clock.tick(FPS) # Caps the frame rate

mainMenuScreen()