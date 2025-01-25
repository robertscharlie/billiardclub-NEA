import pygame
from main import *

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu")

class Button:  # Defines Button class
    def __init__(self, text, fontSize, x, y, padding, callback):
        self.text = text  # Text to display on the button
        self.font = pygame.font.Font("C:/Users/crobe/Documents/GitHub/billiardclub-NEA/Project/other/Orbitron-VariableFont_wght.ttf", fontSize)  # Font for the button text
        self.callback = callback  # Function to call when the button is clicked
        
        self.hovering = False # Set to true if the mouse is hovering over.
        self.clicked = False

        self.boxColour = "white"  # Button colour
        self.boxColourClicked = "grey" # Button colour when clicked
        self.textColour = "black" # Text colour when the mouse is not hovering over
        self.textColourHovering = "red" # Text colour when the mouse is hovering over

        self.textSurface = self.font.render(self.text, True, self.textColour) # Render the button text
        # Rectangle representing the button's position and size
        self.rect = pygame.Rect(x, y, self.textSurface.get_width() + padding, self.textSurface.get_height() + padding)

    def draw(self):
        textColour = ""
        boxColour = ""
        if self.hovering:  # Check if the button is being hovered over
            textColour = self.textColourHovering  # Set textColour to hovering colour
        else:
            textColour = self.textColour  # Set textColour to default colour
        if self.clicked:  # Check if the button is clicked
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
    def __init__(self, fontSize, pos, spacing, options, functions):  # Initializes the Menu class
        self.fontSize = fontSize  # Font size for the menu options
        self.pos = pos  # Position of the menu
        self.spacing = spacing  # Spacing between menu options
        self.options = options  # List of menu options
        self.functions = functions  # List of functions corresponding to each menu option
        self.buttons = []  # List to store buttons
        self.create_buttons()  # Calls the method to create buttons

    def create_buttons(self):  # Method to create buttons
        increment = self.spacing  # Vertical spacing between buttons
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
                    button.clicked = True  # Set button as clicked
                    button.callback()  # Execute the button's callback function
                else:
                    button.clicked = False  # Set button as not clicked
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # When mouse button is released
            for button in self.buttons:  # Iterate through each button
                button.clicked = False  # Set button as not clicked

        
def runGame():
    print("running game")


def showOptions():
    print("Showing options...")

def quitGame():
    global running
    running = False
    

mainMenu = Menu(60, [100,100], 100, ["Start", "Options", "Quit"], [runGame, showOptions, quitGame]) # create a menu


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        mainMenu.handleEvent(event) # check if any button is clicked
        


    screen.fill("black")
    
    mainMenu.draw() # Draw the menu
    mainMenu.update() # update the menu

    pygame.display.flip() # updates screen

pygame.quit()
