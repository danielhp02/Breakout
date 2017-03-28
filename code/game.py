import pygame, sys
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME

import objects
import levels

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

score = 0

# Initialize game objects
bat = objects.Bat(centreX, windowHeight - 25, pygame, surface, 100, 15) # Will make this wider at some point
ball = objects.Ball(pygame, surface, 15, bat)

# Create bricks
currentLevel = 0
level = levels.level
sampleBrick = objects.Brick(1000,1000,pygame,surface,"black", windowWidth)
colours = list(sampleBrick.colours.keys())
currentColour = -1
linesWithBricks = -1
lineColour = 0

bricks = []
for l in level:
    for iy, line in enumerate(l):
        y = (windowHeight//30) * iy
        if 1 in line:
            linesWithBricks += 1
            if linesWithBricks % levels.colourLines[currentLevel] == 0:
                currentColour += 1
            lineColour = colours[currentColour]
            # print(linesWithBricks, "\n", lineColour)
        for ix, brick in enumerate(line):
            if brick == 1:
                x = (windowWidth//10) * ix
                bricks.append(objects.Brick(x, y, pygame, surface, lineColour, windowWidth))
    break # Please ignore dodgy outer for loop for now

# print(linesWithBricks)
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
            if event.key == pygame.K_r:
                if state != onBat:
                    state = onBat
                    print(score) # Remove when score is displayed

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

        ball.move(windowWidth, windowHeight, onBat, bricks)
        ball.draw()

        bat.move(controlsState["left"], controlsState["right"], windowWidth)
        bat.draw()

    elif state == playing:
        if ball.brickIndex is not None:
            score += bricks[ball.brickIndex].scoreValue
            del bricks[ball.brickIndex]
            ball.brickIndex = None

        for brick in bricks:
            brick.draw()

        ball.move(windowWidth, windowHeight, playing, bricks)
        ball.draw()

        bat.move(controlsState["left"], controlsState["right"], windowWidth)
        bat.draw()

    GAME_TIME.Clock().tick(60)
    pygame.display.update()
