import random

class Location(object):
    def __init__(self, x=0, y=0):
        """ initialize the location"""
        self.setXY(x, y)

    def setXY(self, x, y):
        """ change the location"""
        self.x = x
        self.y = y

    def getX(self):
        """ get X coordinate"""
        return self.x

    def getY(self):
        """ get Y coordinate"""
        return self.y

    def getTuple(self):
        return (self.x,self.y)        

    def __str__(self):
        return str(str(self.x) + ", " + str(self.y))

class World(object):
    def __init__(self, lowerX, upperX, lowerY, upperY):
        """ initialize the size of the world"""
        if (upperX < lowerX):
            lowerX, upperX = upperX, lowerX
        if (upperY < lowerY):
            lowerY, upperY = upperY, lowerY
        self.lowerX = lowerX
        self.upperX = upperX
        self.lowerY = lowerY
        self.upperY = upperY

    def inWorld(self, x, y):
        """ Check if x, y coordinates are valid."""
        if (float(x) != x) or (float(y) != y):
            raise ValueError ("x, y coordinates are not floats")
        if ((self.lowerX <= x <= self.upperX) and
            (self.lowerY <= y <= self.upperY)):
                return True
        return False

    def locationInWorld(self, loc):
        return self.inWorld(loc.getX(), loc.getY())

    def randLoc(self):
        """ return a random location within the world"""
        x = random.randint(self.lowerX, self.upperX)
        y = random.randint(self.lowerY, self.upperY)
        l = Location(x,y)
        return l

