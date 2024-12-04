import pygame


pygame.init()


# Variables
FPS = 60
resolution = (1000, 600) # Screen dimensions
borderName = "sliders.py" # Displays at the top of the program


# Pygame Functions
pygame.display.set_caption(borderName)
screen = pygame.display.set_mode(resolution) # Sets up the display
clock = pygame.time.Clock()


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

    def update(self):
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
        
    def returnValue(self):
        return round(1-self.value, 3)


slider1 = Slider("white", "red", (100,100), 30, 400, 1) # initialises sprite

# Game Loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Checks if user closes program
            pygame.quit()
            exit()
    screen.fill((30, 30, 30)) # Fills the screen with a grey colour
    
    
    slider1.draw(screen)
    slider1.update()
    slider1.returnValue()
    
    pygame.display.flip() # Updates the display
    clock.tick(FPS) # Caps the frame rate

