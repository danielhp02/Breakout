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

fps = 60

# Initialise pygame
pygame.init()

# Initialise display
surface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Breakout")

# Load fonts
if __file__ == 'main.py':
    scoreFont = pygame.font.Font("../assets/fonts/pong_score.ttf", 75)
    statusFont = pygame.font.Font("../assets/fonts/FreeMono.ttf", 75)
    ubuntuFont = pygame.font.Font("../assets/fonts/Ubuntu-R.ttf", 75)
else:
    scoreFont = pygame.font.Font("./assets/fonts/pong_score.ttf", 75)
    statusFont = pygame.font.Font("./assets/fonts/FreeMono.ttf", 75)
    ubuntuFont = pygame.font.Font("./assets/fonts/Ubuntu-R.ttf", 75)

# Load images
if __file__ == 'main.py':
    gameOverImg = pygame.image.load('../assets/gameOver.png')
else:
    gameOverImg = pygame.image.load('./assets/gameOver.png')
gameOverImg.convert() # Apparantly this makes it load slightly faster

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
    global state, previousState
    previousState = state
    state = state_

# Initiate player variables
score = 0

maxLives = 2
lives = 2

# Initialize game objects
bat = objects.Bat(centreX, windowHeight - 25, pygame, surface, 100, 15) # Will make this wider when more complex bouncing is added
ball = objects.Ball(pygame, surface, 15, bat)

def loseLife():
    global lives

    lives -= 1
    if lives < 0:
        setState(gameOver)
    else:
        setState(onBat)

# Brick/Level related things
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
    except IndexError: # This means that the last level has been completed and therefore the game is won
        setState(gameWon)

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

# Display Info
def drawPaused():
    pauseText = 'PAUSED'
    pauseObj = statusFont.render(pauseText, 1, (200,200,200))
    pausePosition = (windowWidth/2 - statusFont.size(pauseText)[0]/2, windowHeight/2 - statusFont.size(pauseText)[1]/2)
    surface.blit(pauseObj, pausePosition)

def drawScore(position=None, font=None, colour='grey'):
    global score

    if colour == 'grey':
        scoreColour = (127,127,127)
    elif colour == 'white':
        scoreColour = (255,255,255)
    if font is None:
        font = scoreFont

    scoreText = str(score)
    if position is None:
        if font == scoreFont:
            scorePosition = (windowWidth/2 - font.size(scoreText)[0]/4, bat.y - 200)
        else:
            scorePosition = (windowWidth/2 - font.size(scoreText)[0]/2, bat.y - 200)
    else:
        if position[0] is None:
            if font == scoreFont:
                scorePosition = (windowWidth/2 - font.size(scoreText)[0]/4, position[1])
            else:
                scorePosition = (windowWidth/2 - font.size(scoreText)[0]/2, position[1])
        elif position[1] is None:
            if font == scoreFont:
                scorePosition = (position[0], windowWidth/2 - font.size(scoreText)[0]/4) # scoreFont y centring untested
            else:
                scorePosition = (position[0], windowWidth/2 - font.size(scoreText)[0]/2)
        else:
            scorePosition = position
    scoreObj = font.render(scoreText, 1, scoreColour)
    surface.blit(scoreObj, scorePosition)

def resetGame(): # Important Lesson: When you are trying to reset a game, remember global
    global bricks, currentLevel, score, lives
    bricks = []
    currentLevel = -1
    score = 0
    lives = maxLives
    setState(onBat)

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
                if state == gameOver:
                    resetGame()
                elif state == gamePaused:
                    state = previousState
                else:
                    setState(gamePaused)
            if event.key == pygame.K_t: # ;)
                if fps == 60:
                    fps = 240 # x4 speed
                else:
                    fps = 60

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
        drawPaused()

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

        if ball.rockBottom:
            loseLife()
            ball.rockBottom = False
            ball.dy = -3

    elif state == gameWon:
        print("You Win! Your final score was " + str(score))
        quitGame() # Remove later

    elif state == gameOver:
        # print("Game over! You lost with a final score of " + str(score))
        # quitGame()
        drawBricks()
        surface.blit(gameOverImg, (0,0))
        drawScore((None,240), ubuntuFont, 'white')

        bat.move(controlsState["left"], controlsState["right"], windowWidth)
        bat.draw()

    GAME_TIME.Clock().tick(fps) # 60 seems best
    pygame.display.update() # Update the screen
