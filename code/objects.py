import random

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

        self.colour = (255, 255, 255)

        self.score = 0

        # The number of frames the game goes without checking for the collision with
        # the bat to avoid the ball getting stuck
        self.cfAmount = 20
        self.collisionFrames = self.cfAmount

    # Reset the ball after a point is scored
    def reset(self):
        # Reset ball position
        self.x = self.bat.x + self.bat.width // 2
        self.y = self.bat.y - self.radius

        self.setSpeed()

    # Check for collisions with the bats and the edges of the window
    def checkForCollisions(self, windowWidth, windowHeight, blocks):
        # Check For collision with left and right boundaries
        if self.x - self.radius < 0 or self.x + self.radius > windowWidth:
            self.dx *= -1

        # Bounce off the top boundary
        if self.y - self.radius < 0:
            self.dy *= -1

        # Bottom boundary - a life is lost
        # elif self.y + self.radius > windowHeight:
        #     self.loseLife()

        # Bat - Note: the collision is only with the innermost side.
        if self.collisionFrames <= 0:
            if self.y + self.radius > self.bat.y and self.bat.x < self.x < self.bat.x + self.bat.width:
                self.dy *= -1
                self.collisionFrames = self.cfAmount
        else:
            self.collisionFrames -= 1

        # blocks
        # for whatever

    def move(self, windowWidth, windowHeight, state):
        if state == "onBat":
            self.x = self.bat.x + self.bat.width // 2
            self.y = self.bat.y - self.radius

        elif state == "playing":
            blocks = None
            self.checkForCollisions(windowWidth, windowHeight, blocks)
            self.x += self.dx
            self.y += self.dy

    def draw(self):
        self.pygame.draw.circle(self.surface, self.colour, (int(round(self.x)), int(round(self.y))), self.radius)

class Bat(object):

    def __init__(self, startX, y, pygame, surface, width, height):
        self.x = startX
        self.y = y

        # These are so the bats can interact with the game without pygame being
        # imported or this class having to be in the main file.
        self.pygame = pygame
        self.surface = surface

        self.width = width
        self.height = height

        self.speed = 3 # The speed the bat will do either way
        self.dx = 0 # The speed the bat is currently doing

        self.colour = (255, 255, 255)

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

        colours = {"red":    (255, 0, 0),
                   "green":  (0, 255, 0),
                   "blue":   (0, 0, 255),
                   "yellow": (255, 255, 0),
                   "cyan":   (0, 255, 255),
                   "magenta":(255, 0, 255),
                   "white":  (255, 255, 255),
                   "grey":   (127, 127, 127)
                   }

        try:
            self.colour = colours[colour]
        except KeyError:
            print("'" + colour + "'", "is not a valid colour.")
            self.colour = colours["white"]

        self.width = windowWidth/10
        self.height = self.width // 4

    def draw(self):
        self.pygame.draw.rect(self.surface, self.colour, (self.x, self.y, self.width, self.height))
