
class Sighting(object):
    def __init__(self, loc, animalID):
        """ initialize the sighting""" 
        self.animalID = animalID
        self.loc = loc
    def __str__(self):
        return (str(self.loc) + " " + self.animalID)
    def getAnimalID(self):
        return self.animalID


       
