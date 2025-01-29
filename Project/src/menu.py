import pygame
from main import *


# Initialize Pygame
pygame.init()

player1Name = "Player 1"
player2Name = "Player 2"

player1Colour = "red"
player2Colour = "blue"


# Pygame Functions
pygame.display.set_caption(borderName)
screen = pygame.display.set_mode(resolution) # Sets up the display
clock = pygame.time.Clock()

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

class HorizontalSlider(pygame.sprite.Sprite): # Slider Class
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
        pygame.draw.rect(screen, self.sliderColour, self.rect, 0, 10)  # Draw the slider rectangle
        if self.sliderType == "colourPicker":  # Check if the slider type is a colour picker
            for i in range(self.width-18):  # Iterate through the width of the slider
                colour = pygame.Color(0)  # Create a new colour object
                colour.hsla = (int(360 * i / self.width), 100, 50, 100)  # Set the colour based on the position
                pygame.draw.rect(screen, colour, (self.x+i, self.y, self.width - i, self.height), 0, 10)  # Draw the colour rectangle
        
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

def runGame(computerPlaying, sandbox): # Function to start a new game
    print(player1Name)
    newGame(computerPlaying, sandbox, player1Name, player2Name, player1Colour, player2Colour)

def quitGame(): # Function to quit the game
    pygame.quit()
    exit()
    

mainMenu = Menu(60, [50,50], ["Start", "Options", "Quit"], ["gameModeScreen()", "optionsScreen()", "quitGame()"]) # create a menu
gameModeMenu = Menu(60, [50,50], ["Player vs Player", "Player vs AI", "Sandbox Mode", "Back"], ["runGame(False, False)", "runGame(True, False)", "runGame(False, True)", "mainMenuScreen()"]) # create a menu
optionsMenu = Menu(60, [50,50], ["Customise Game", "Volume Control", "Back"], ["customisationScreen()", "mainMenuScreen()", "mainMenuScreen()"]) # create a menu

customisationMenu = Menu(60, [50,50], ["Customise Game", "Back"], ["customisationScreen()", "optionsScreen()"]) # create a menu

mainMenuScreen()