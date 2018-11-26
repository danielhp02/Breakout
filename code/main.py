import pygame
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME
import sys

import objects
import levels
import colours

# Initialise window variables
windowWidth = 800
windowHeight = 600
centreX = windowWidth/2
centreY = windowHeight/2

overlayOpacity = 100
backgroundColour = colours.black

fps = 60

# Initialise pygame
pygame.init()
clock = GAME_TIME.Clock()

# Initialise display
surface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Breakout")

# Load images and fonts. This setup is so that the correct location is used for
# loading assets no matter where the program is run from
try:
    if __file__ == 'main.py': # Only works in terminal, but screw idle (for now)
        scoreFont = pygame.font.Font("../assets/fonts/pong_score.ttf", 75)
        statusFont = pygame.font.Font("../assets/fonts/FreeMono.ttf", 75)
        ubuntuFont = pygame.font.Font("../assets/fonts/Ubuntu-R.ttf", 75)
        ubuntuFontSmall = pygame.font.Font("../assets/fonts/Ubuntu-R.ttf", 30)
    else:
        scoreFont = pygame.font.Font("./assets/fonts/pong_score.ttf", 75)
        statusFont = pygame.font.Font("./assets/fonts/FreeMono.ttf", 75)
        ubuntuFont = pygame.font.Font("./assets/fonts/Ubuntu-R.ttf", 75)
        ubuntuFontSmall = pygame.font.Font("./assets/fonts/Ubuntu-R.ttf", 30)
except OSError:
    scoreFont = pygame.font.Font("../assets/fonts/pong_score.ttf", 75)
    statusFont = pygame.font.Font("../assets/fonts/FreeMono.ttf", 75)
    ubuntuFont = pygame.font.Font("../assets/fonts/Ubuntu-R.ttf", 75)
    ubuntuFontSmall = pygame.font.Font("../assets/fonts/Ubuntu-R.ttf", 30)

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

def centreText(pos, font, text):
    if pos is None:
        position = (windowWidth/2 - font.size(text)[0]/2, windowHeight/2 - font.size(text)[1]/2)
    elif pos[0] is None:
        position = (windowWidth/2 - font.size(text)[0]/2, pos[1])
    elif pos[1] is None:
        position = (pos[0], windowHeight/2 - font.size(text)[1]/2)
    else:
        position = pos
    return position

def drawText(position, font, text, colour):
    textObj = font.render(text, 1, colour)
    surface.blit(textObj, position)

def drawRect(colour, x, y, width, height):
    s = pygame.Surface((width,height))  # the size of your rect
    s.set_alpha(colour[3])                # alpha level
    s.fill(colour[:3])           # this fills the entire surface
    surface.blit(s, (x,y))    # (0,0) are the top-left coordinates

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
        ball.setSpeed()
        setState(onBat)

def drawLives(asText=False, position=None):
    global lives

    if asText is True:
        lives_ = lives + 1
        font = ubuntuFont
        lifeText = str(lives_)
        lifePosition = centreText(position, font, lifeText)
        drawText(lifePosition, font, lifeText, colours.white)
    else:
        for l in range(lives):
            pygame.draw.circle(surface, colours.grey, (40*l + 25, 20), ball.radius)

        if lives == 0:
            pygame.draw.circle(surface, colours.red, (40*lives + 25, 20), ball.radius)
        elif lives == 1:
            pygame.draw.circle(surface, colours.orange, (40*lives + 25, 20), ball.radius)
        elif lives == 2:
            pygame.draw.circle(surface, colours.green, (40*lives + 25, 20), ball.radius)

# Brick/Level related things
currentLevel = -1
level = levels.level
sampleBrick = objects.Brick(1000,1000,pygame,surface,"black", windowWidth)
levelColours = list(sampleBrick.colours.keys())

bricks = []
def newLevel(level_):
    global score
    if level_ > 0:
        score += (lives+1)*15
    currentColour = -1
    linesWithBricks = -1

    try:
        for iy, line in enumerate(level[level_]):
            y = (windowHeight//30) * iy
            if 1 in line:
                linesWithBricks += 1
                if linesWithBricks % levels.colourLines[currentLevel] == 0:
                    currentColour += 1
                lineColour = levelColours[currentColour]
            for ix, brick in enumerate(line):
                if brick == 1:
                    x = (windowWidth//10) * ix
                    bricks.append(objects.Brick(x, y, pygame, surface, lineColour, windowWidth))
    except IndexError: # This means that the last level has been completed and therefore the game is won
        setState(gameWon)

def displayCurrentLevel(inGame=True, position=None):
    global currentLevel

    if inGame:
        levelPosition = (650,5)
        levelText = "Level " + str(currentLevel + 1)
        levelFont = ubuntuFontSmall
        drawText(levelPosition, levelFont, levelText, colours.grey)
    else:
        levelFont = ubuntuFont
        levelText = str(currentLevel + 1)
        levelPosition = centreText(position, levelFont, levelText)
        drawText(levelPosition, levelFont, levelText, colours.white)

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
    pausePosition = (windowWidth/2 - statusFont.size(pauseText)[0]/2, windowHeight/2 - statusFont.size(pauseText)[1]/2)
    drawText(pausePosition, statusFont, pauseText, colours.lightGrey)

def drawScore(position=None, font=None, colour='grey'):
    global score

    if colour == 'grey':
        scoreColour = colours.grey
    elif colour == 'white':
        scoreColour = colours.white
    if font is None:
        font = scoreFont

    scoreText = str(score)
    if position is None: # I would replace this with centreText but the scoreFont is weird
        if font == scoreFont:
            scorePosition = (windowWidth/2 - font.size(scoreText)[0]/4, bat.y - 200)
        else:
            scorePosition = (windowWidth/2 - font.size(scoreText)[0]/2, bat.y - 200)
    elif position[0] is None:
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
    drawText(scorePosition, scoreFont, scoreText, scoreColour)

# Win/lose screens
menuFont = ubuntuFont
def endGameBackground():
    if state == gameWon:
        drawRect((0,255,0,overlayOpacity), 0, 0, surface.get_width(), surface.get_height())
    elif state == gameOver:
        drawRect((255,0,0,overlayOpacity), 0, 0, surface.get_width(), surface.get_height())

def endGameHeading():
    global state

    statusFont.set_bold(True)
    if state == gameWon:
        headingText = "You win!"
    elif state == gameOver:
        headingText = "You lose!"
    headingPosition = centreText((None,15), statusFont, headingText)
    drawText((headingPosition), statusFont, headingText, colours.white)
    statusFont.set_bold(False)

def endGameStats():
    global state

    statText = []
    if state == gameWon:
        statText.append("You finished with a")
        statText.append("score of " + str(score) + " points")
        statText.append("and with " + str(lives) + " lives")
        statText.append("remaining.")
    elif state == gameOver:
        statText.append("You finished with a")
        statText.append("score of " + str(score) + " points")
        statText.append("and on level " + str(currentLevel + 1) + ".")
    for idx,text in enumerate(statText):
        statPosition = centreText((None,75*idx + 120), menuFont, text)
        drawText(statPosition, menuFont, text, colours.white)

def endGameInfo():
    infoText = ["Hit Enter to play", "again."]
    for idx, text in enumerate(infoText):
        infoPostion = centreText((None, 30*idx+475), ubuntuFontSmall, text)
        drawText(infoPostion, ubuntuFontSmall, text, colours.white)

def drawEndGameOverlay():
    endGameBackground()
    endGameHeading()
    endGameStats()
    endGameInfo()

def resetGame(): # Important Lesson: When you are trying to reset a game, remember global
    global bricks, currentLevel, score, lives
    bricks = []
    currentLevel = -1
    score = 0
    lives = maxLives
    ball.setSpeed()
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

    # React to system inputs
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
            if event.key == pygame.K_r: # Reset the ball without losing a life
                if state != onBat:
                    setState(onBat)
                    ball.setSpeed()
            if event.key == pygame.K_RETURN: # Pause or reset the game
                if state == gameOver or state == gameWon:
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
            if event.key == pygame.K_k: # To test win screen/code
                setState(gameWon)
            if event.key == pygame.K_l: # To test lose screen/code
                setState(gameOver)

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
        drawLives()
        drawBricks()
        ball.draw()
        bat.draw()
        drawPaused()

    elif state == onBat:
        if len(bricks) == 0:
            currentLevel += 1
            newLevel(currentLevel)

        drawScore()
        drawLives()
        displayCurrentLevel()

        drawBricks()

        ball.move(windowWidth, windowHeight, onBat, bricks)
        ball.draw()

        bat.move(controlsState["left"], controlsState["right"], windowWidth)
        bat.draw()

    elif state == playing:
        if len(bricks) == 0:
            setState(onBat)

        drawScore()
        drawLives()
        displayCurrentLevel()

        destroyBricks()
        drawBricks()

        ball.move(windowWidth, windowHeight, playing, bricks)
        ball.draw()

        bat.move(controlsState["left"], controlsState["right"], windowWidth)
        bat.draw()

        if ball.rockBottom:
            loseLife()
            ball.rockBottom = False

    elif state == gameWon:
        drawBricks()
        bat.move(controlsState["left"], controlsState["right"], windowWidth)
        bat.draw()
        drawEndGameOverlay()

    elif state == gameOver:
        drawBricks()
        bat.move(controlsState["left"], controlsState["right"], windowWidth)
        bat.draw()
        drawEndGameOverlay()

    clock.tick(fps) # 60 seems best for standard play
    pygame.display.update() # Update the screen
