import math

class Camera(object):
    def __init__(self, loc, radius):
        """ set camera location and visibility radius"""
        self.loc = loc
        if (radius <= 0):
            raise AttributeError ("the radius for the camera must be > 0")
        self.radius = radius
        self.setLoc(loc)

    def setLoc(self, loc):
        self.loc = loc
        self.lowerVisibleX = loc.x - self.radius
        self.upperVisibleX = loc.x + self.radius
        self.lowerVisibleY = loc.y - self.radius
        self.upperVisibleY = loc.y + self.radius
        self.x = loc.x
        self.y = loc.y

    def canSee(self, otherLoc):
        if ((self.lowerVisibleX <= otherLoc.x <= self.upperVisibleX) and
           (self.lowerVisibleY <= otherLoc.y <= self.upperVisibleY)):
            return True
        return False
  
    def makesSighting(self, Sighting):
        return self.canSee(Sighting.loc)

    def measureDist(self, otherLoc):
        dist = math.sqrt(((self.x - otherLoc.x) * (self.x - otherLoc.x)) + ((self.y - otherLoc.y) * (self.y - otherLoc.y)))
        dist = dist / self.radius
        if (dist == 0.0):
            distScore = 0.0
        else:
            distScore = 1.0 / dist
        return distScore
          
    def distSighting(self, Sighting):
        return self.measureDist(Sighting.loc)
  
    def __str__(self):
        return str(self.loc) 

    def getLowX(self):
        return self.lowerVisibleX

    def getLowY(self):
        return self.lowerVisibleY

    def getUpperX(self):
        return self.upperVisibleX

    def getUpperY(self):
        return self.upperVisibleY
