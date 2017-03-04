import pygame, sys
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME

import objects

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
controlsState = {'left': False, 'right': False}

# Game states
onBat, playing, gameOver, gameWon = "onBat", "playing", "gameOver", "gameWon" # All possible states
state = onBat

# Initialize game objects
bat = objects.Bat(centreX, windowHeight - 25, pygame, surface, 100, 15)
ball = objects.Ball(pygame, surface, 15, bat)

# Create bricks
# sampleBrick = objects.Brick(centreX, centreY, pygame, surface, "white", windowHeight) # Sample brick for data
bricks = []
for b in range(0, windowWidth+1, windowWidth/10):
    bricks.append(objects.Brick(b, centreY, pygame, surface, "yellow", windowWidth))

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
            if event.key == pygame.K_UP:
                if state == onBat:
                    state = playing

            if event.key == pygame.K_ESCAPE:
                quitGame()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                controlsState["left"] = False

            if event.key == pygame.K_RIGHT:
                controlsState["right"] = False

        if event.type == pygame.QUIT:
            quitGame()

    # Check current state and act accordingly
    if state == onBat:
        for brick in bricks:
            brick.draw()

        ball.move(windowWidth, windowHeight, onBat)
        ball.draw()

        bat.move(controlsState["left"], controlsState["right"], windowWidth)
        bat.draw()

    elif state == playing:
        for brick in bricks:
            brick.draw()

        ball.move(windowWidth, windowHeight, playing)
        ball.draw()

        bat.move(controlsState["left"], controlsState["right"], windowWidth)
        bat.draw()

    GAME_TIME.Clock().tick(60)
    pygame.display.update()
