import pygame
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME

# Initialise window variables
windowWidth = 800
windowHeight = 600
centreX = windowWidth/2
centreY = windowHeight/2

backgroundColour = (0, 0, 0)

# Initialise pygame
pygame.init()

# Initialise display
surface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Breakout")

# Store states of keys that cause continuous movement
controlsState = {left: False, right: False}

# Initialize game objects

# Quit and uninitialise the game
def quitGame():
    pygame.quit()
    sys.exit()

# Main loop
while True:

    # Clear screen
    surface.fill(backgroundColour)

    for event in GAME_EVENTS.get():

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                controlsState["left"] = True
                controlsState["right"] = False
            if event.key == pygame.K_RIGHT:
                controlsState["right"] = True
                controlsState["left"] = False

            if event.key == pygame.K_ESCAPE:
                quitGame()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                controlsState["left"] = False

            if event.key == pygame.K_RIGHT:
                controlsState["right"] = False

        if event.type == pygame.QUIT:
            quitGame()

    GAME_TIME.Clock().tick(60)
    pygame.display.update()
