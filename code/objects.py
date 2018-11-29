import random
from collections import OrderedDict

import colours

class Ball():

    def setSpeed(self):
        # Getting a random direction for the ball to start in
        self.dx = random.choice([-3, 3])
        self.dy = -3


    def __init__(self, pygame, surface, radius, bat):
        # These are so the ball can interact with the game without pygame being
        # imported or this class having to be in the main file.
        self.pygame = pygame
        self.surface = surface

        self.radius = radius

        # So the ball can interact with the bat
        self.bat = bat

        self.x = self.bat.x + self.bat.width / 2
        self.y = self.bat.y + self.radius

        self.setSpeed()

        self.colour = colours.white

        self.score = 0

        self.brickIndex = None
        self.rockBottom = False

        # The number of frames the game goes without checking for the collision with
        # the bat to avoid the ball getting stuck
        self.cfAmount = 20
        self.collisionFrames = self.cfAmount

    # Check for collisions with the bats and the edges of the window
    def checkForCollisions(self, windowWidth, windowHeight, bricks):
        # Check For collision with left and right boundaries
        if self.x - self.radius < 0 or self.x + self.radius > windowWidth:
            self.dx *= -1

        # Bounce off the top boundary
        if self.y - self.radius < 0:
            self.dy *= -1

        # Bottom boundary - a life is lost
        elif self.y + self.radius > windowHeight:
            self.rockBottom = True

        # Bat
        if self.collisionFrames <= 0:
            if (self.y + self.radius > self.bat.y and self.y - self.radius < self.bat.y + self.bat.height and
                self.x in range(int(self.bat.x), int(self.bat.x) + int(self.bat.width))):
                self.dy *= -1
                self.collisionFrames = self.cfAmount
            elif (self.x + self.radius > self.bat.x and self.x - self.radius < self.bat.x + self.bat.width and
                self.y in range(int(self.bat.y), int(self.bat.y) + int(self.bat.height))):
                self.dx *= -1
                self.collisionFrames = self.cfAmount
        else:
            self.collisionFrames -= 1

        # blocks
        for i, brick in enumerate(bricks):
            if (self.x + self.radius > brick.x and self.x - self.radius < brick.x + brick.width and
                self.y in range(int(brick.y), int(brick.y) + brick.height)):
                self.dx *= -1
                self.brickIndex = i
            elif (self.y + self.radius > brick.y and self.y - self.radius < brick.y + brick.height and
                self.x in range(brick.x, brick.x + brick.width)):
                self.dy *= -1
                self.brickIndex = i


    def move(self, windowWidth, windowHeight, state, bricks):
        if state == "onBat":
            self.x = self.bat.x + self.bat.width // 2
            self.y = self.bat.y - self.radius

        elif state == "playing":
            self.checkForCollisions(windowWidth, windowHeight, bricks)
            self.x += self.dx
            self.y += self.dy

    def draw(self):
        self.pygame.draw.circle(self.surface, self.colour, (int(round(self.x)), int(round(self.y))), self.radius)

class Bat(object):

    def __init__(self, startX, y, pygame, surface, width, height):
        self.x = startX - width/2
        self.y = y

        # These are so the bats can interact with the game without pygame being
        # imported or this class having to be in the main file.
        self.pygame = pygame
        self.surface = surface

        self.width = width
        self.height = height

        self.speed = 4 # The speed the bat will do either way
        self.dx = 0 # The speed the bat is currently doing

        self.colour = colours.white

    def move(self, left, right, rightLimit):
        if left and self.x > 0:
            self.dx = -self.speed
        elif right and self.x + self.width < rightLimit:
            self.dx = self.speed
        else:
            self.dx = 0

        self.x += self.dx

    def draw(self):
        self.pygame.draw.rect(self.surface, self.colour, (self.x, self.y, self.width, self.height))

class Brick():
    def __init__(self, x, y, pygame, surface, colour, windowWidth):
        self.x = x
        self.y = y

        self.pygame = pygame
        self.surface = surface

        self.colours = OrderedDict([
            ("red",    colours.red),
            ("orange", colours.orange),
            ("yellow", colours.yellow),
            ("green",  colours.green),
            ("blue",   colours.blue),

            ("cyan",   colours.cyan),
            ("magenta",colours.magenta),
            ("grey",   colours.grey),
            ("white",  colours.white),
            ("black",  colours.black)
            ])

        try:
            self.colour = self.colours[colour]
        except KeyError:
            print("'" + colour + "'", "is not a valid colour. Brick will be invisible, but present.")
            self.colour = colours.black # black if failed

        self.scoreValues = {
            "red": 7,
            "orange": 7,
            "yellow": 4,
            "green": 4,
            "blue": 1,
            "cyan": 1,
            "black": 0
            }

        try:
            self.scoreValue = self.scoreValues[colour]
        except KeyError:
            print("'" + colour + "'", "is not a scorable colour. Brick will be worth 0 points.")
            self.scoreValue = 0

        self.width = windowWidth // 10
        self.height = self.width // 4

    def draw(self):
        self.pygame.draw.rect(self.surface, self.colour, (self.x, self.y, self.width, self.height))

class button():
    def __init__(self, pygame, surface, colour, rectangle, text, font):
        self.pygame = pygame
        self.surface = surface
        self.colour = colour
        self.rectangle = self.pygame.Rect(rectangle)
        self.text = text
        self.font = font

        self.textObj = self.font.render(self.text, 1, self.colour)

        self.position = (self.rectangle.width/2 - self.font.size(self.text)[0]/2, self.rectangle.height/2 - self.font.size(self.text)[1]/2)

    def draw(self):
        self.pygame.draw.rect(self.surface, self.colour, self.rectangle)
        self.surface.blit(self.textObj, self.position)

    def isClicked(self):
        if button.collidepoint(mouse_pos):
            return True

# class Menu():
#     def __init__(self, pygame, surface, title, backgroundColour, titleFont, normalFont, options):
#         self.pygame = pygame
#         self.surface = surface
#         self.title = title
#         self.backgroundColour = backgroundColour
#         self.titleFont = titleFont
#         self.normalFont = normalFont
#         self.options = options
#
#     def draw(self):
#         # Calculate position of heading
#         self.titleFont.set_bold(True)
#         headingPosition = surface.get_width()/2 - self.titleFont.size(self.title)[0]/2, self.titleFont.size(self.title)[1]/3
#
#         # Calculate position of options
#         optionPositions = []
#         for option in self.options:
#             optionPositions.append(surface.get_width()/2 - self.normalFont.size(option)[0]/2, self.normalFont.size(option)[1]/3)
