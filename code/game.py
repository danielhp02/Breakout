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

scoreFont = pygame.font.SysFont("pong_score", 75)
# scoreFont.setB

# Store states of keys that cause continuous movement
controlsState = {'left': False, 'right': False}

# Game states
onBat = "onBat"
playing = "playing"
gameOver = "gameOver"
gameWon = "gameWon"
gamePaused = "gamePaused"
state = onBat
previousState = gamePaused

def setState(state_):
    global state
    previousState = state
    state = state_

score = 0

# Initialize game objects
bat = objects.Bat(centreX, windowHeight - 25, pygame, surface, 100, 15) # Will make this wider when more complex bouncing is added
ball = objects.Ball(pygame, surface, 15, bat)

# Create bricks
currentLevel = -1
level = levels.level
sampleBrick = objects.Brick(1000,1000,pygame,surface,"black", windowWidth)
colours = list(sampleBrick.colours.keys())

bricks = []
def newLevel(level_):
    currentColour = -1
    linesWithBricks = -1

    try:
        for iy, line in enumerate(level[level_]):
            y = (windowHeight//30) * iy
            if 1 in line:
                linesWithBricks += 1
                if linesWithBricks % levels.colourLines[currentLevel] == 0:
                    currentColour += 1
                lineColour = colours[currentColour]
            for ix, brick in enumerate(line):
                if brick == 1:
                    x = (windowWidth//10) * ix
                    bricks.append(objects.Brick(x, y, pygame, surface, lineColour, windowWidth))
    except IndexError:
        setState(gameWon)
        print("You Win! Your final score was " + score)
        quitGame() # Remove later

def drawBricks():
    for brick in bricks:
        brick.draw()

def destroyBricks():
    global score

    if ball.brickIndex is not None:
        score += bricks[ball.brickIndex].scoreValue
        del bricks[ball.brickIndex]
        ball.brickIndex = None
        # print(len(bricks))

def drawScore():
    global score

    scoreText = str(score)
    scoreObj = scoreFont.render(scoreText, 1, (127,127,127))
    scorePosition = (windowWidth/2 - scoreFont.size(scoreText)[0]/4, bat.y - 200) #
    surface.blit(scoreObj, scorePosition)

# Quit and uninitialise the game
def quitGame():
    # print(score)
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
                    setState(playing)
            if event.key == pygame.K_r:
                if state != onBat:
                    setState(onBat)
            if event.key == pygame.K_RETURN:
                if state == gamePaused and previousState is not None:
                    state = previousState
                else:
                    setState(gamePaused)

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
    if state == gamePaused:
        drawScore()
        drawBricks()
        ball.draw()
        bat.draw()

    elif state == onBat:
        if len(bricks) == 0:
            currentLevel += 1
            newLevel(currentLevel)

        drawScore()

        drawBricks()

        ball.move(windowWidth, windowHeight, onBat, bricks)
        ball.draw()

        bat.move(controlsState["left"], controlsState["right"], windowWidth)
        bat.draw()

    elif state == playing:
        if len(bricks) == 0:
            setState(onBat)

        drawScore()

        destroyBricks()
        drawBricks()

        ball.move(windowWidth, windowHeight, playing, bricks)
        ball.draw()

        bat.move(controlsState["left"], controlsState["right"], windowWidth)
        bat.draw()

    GAME_TIME.Clock().tick(60)
    pygame.display.update()
