import random
from collections import OrderedDict

import colours

class Ball(object):

    # def setSpeed(self):
    #     # Getting a random direction for the ball to start in
    #     self.dx = random.choice([-3, 3])
    #     self.dy = -3


    def __init__(self, pygame, surface, radius, bat):
        # These are so the ball can interact with the game without pygame being
        # imported or this class having to be in the main file.
        self.pygame = pygame
        self.surface = surface


        self.radius = radius

        # So the ball can interact with the bat
        self.bat = bat

        self.position = self.pygame.math.Vector2(self.bat.position.x + self.bat.width / 2, self.bat.position.y + self.radius)

        self.direction = self.pygame.math.Vector2(0.707, -0.707)
        self.speed = 255
        # self.setSpeed()

        self.colour = colours.white

        self.brickIndex = None
        self.rockBottom = False

        # The number of frames the game goes without checking for the collision with
        # the bat to avoid the ball getting stuck
        self.cfAmount = 20
        self.collisionFrames = self.cfAmount

    def Vector2(self,x,y):
        return self.pygame.math.Vector2(x,y)

    # Check for collisions with the bats and the edges of the window
    def checkForCollisions(self, windowWidth, windowHeight, bricks):
        # Check For collision with left and right boundaries
        if self.position.x - self.radius < 0 or self.position.x + self.radius > windowWidth:
            self.direction.x *= -1

        # Bounce off the top boundary
        if self.position.y - self.radius < 0:
            self.direction.y *= -1

        # Bottom boundary - a life is lost
        elif self.position.y + self.radius > windowHeight:
            self.rockBottom = True

        # Bat
        if self.collisionFrames <= 0:
            if ((self.position.x > self.bat.position.x - self.radius) and
                (self.position.x < (self.bat.position.x + self.radius + self.bat.width)) and
                (self.position.y < self.bat.position.y) and
                (self.position.y > (self.bat.position.y - self.radius))):

                normal = self.Vector2(0, -1)

                dist = self.bat.width
                ballLocation = self.position.x - self.bat.position.x
                pct = ballLocation / dist

                if pct < 0.33:
                    normal = self.Vector2(-0.196, -0.981)
                elif pct > 0.66:
                    normal = self.Vector2(0.196, -0.981)

                self.direction.reflect_ip(normal)

                self.collisionFrames = self.cfAmount
            # elif (self.position.x + self.radius > self.bat.position.x and self.position.x - self.radius < self.bat.position.x + self.bat.width and
            #     self.position.y in range(int(self.bat.position.y), int(self.bat.position.y) + int(self.bat.height))):
            #     self.direction.x *= -1
            #     self.collisionFrames = self.cfAmount
        else:
            self.collisionFrames -= 1

    #     # blocks
    #     for i, brick in enumerate(bricks):
    #         if (self.x + self.radius > brick.x and self.x - self.radius < brick.x + brick.width and
    #             self.y in range(int(brick.y), int(brick.y) + brick.height)):
    #             self.dx *= -1
    #             self.brickIndex = i
    #         elif (self.y + self.radius > brick.y and self.y - self.radius < brick.y + brick.height and
    #             self.x in range(brick.x, brick.x + brick.width)):
    #             self.dy *= -1
    #             self.brickIndex = i


    def move(self, windowWidth, windowHeight, state, bricks, deltaTime):
        if state == "onBat":
            self.position.x = self.bat.position.x + self.bat.width // 2
            self.position.y = self.bat.position.y - self.radius

        elif state == "playing":
            self.checkForCollisions(windowWidth, windowHeight, bricks)
            self.position += self.direction * self.speed * deltaTime

    def draw(self):
        self.pygame.draw.circle(self.surface, self.colour, (int(self.position.x), int(self.position.y)), self.radius)

class Bat(object):

    def __init__(self, startX, y, pygame, surface, width, height):
        # These are so the bats can interact with the game without pygame being
        # imported or this class having to be in the main file.
        self.pygame = pygame
        self.surface = surface

        self.position = self.pygame.math.Vector2(startX - width/2, y)

        self.width = width
        self.height = height

        self.speed = 155 # The speed the bat will do either way left or right

        self.colour = colours.white

    def move(self, left, right, rightLimit, deltaTime):
        if left and self.position.x > 0:
            self.position.x -= self.speed * deltaTime
        elif right and self.position.x + self.width < rightLimit:
            self.position.x += self.speed * deltaTime

    def draw(self):
        self.pygame.draw.rect(self.surface, self.colour, (self.position.x, self.position.y, self.width, self.height))

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
