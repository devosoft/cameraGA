import camera
import random
import world
import math
import convexHull

class GA (object):
    def __init__ (self, numGen, popSize, crossPer, mutPer, fitFunc, selection=0, runOut="run.log", bestOut="best.log"):
        self.pop = []
        self.numGen = numGen
        self.crossPer = crossPer
        self.mutPer = mutPer
        self.popSize = popSize
        self.fitFunc = fitFunc
        self.runOut = runOut
        self.bestOut = bestOut
        self.selection = selection
            
    def __str__ (self):
        mystr = ""
        for i in self.pop:
            mystr +=  str(i.rep) + " " + str(i.getFitness()) + "\n"
        return mystr

    def initPop (self, world, camCount, camRad, sightings):
        self.world = world
        self.camCount = camCount
        self.camRad = camRad
        self.sightings = sightings
        for i in range(0, self.popSize):
            self.pop.append(Individual(self.world, self.camCount, self.camRad,
                                       self.fitFunc, self.sightings))
            
    def run (self):
        runout = open(self.runOut, 'w')
        bestout = open(self.bestOut, 'w')
        runout.write('generation fitness [individuals seen]\n')
        print('\ngeneration fitness [individuals seen]')
        for i in range(0, self.numGen):
            # create offspring
            offspring = []
            offspringNum =  ((self.crossPer) * self.popSize)
            for j in range(0, math.floor(offspringNum/2)):
                ind1 = self.fps()
                ind2 = self.fps()
                offspring.extend(ind1.crossover(ind2))

            for o in range(0,len(offspring)):
                offspring[o].mutate(self.mutPer)

            self.pop += offspring
            
            newpop = []
            while len(newpop) < self.popSize:
                if (self.selection == 0):
                    newpop.extend(self.tournament_selection(2,1))
                else:
                    newpop.append(self.fps())
            self.pop = []
            self.pop = newpop
            self.pop.sort()
            s = str(i) + ' ' + str(self.pop[-1].getFitness())  + ' ' + str(self.pop[-1].getIDs()) + '\n'
            runout.write(s)
            print(str(i) + ' ' + str(self.pop[-1].getFitness()) + ' ' + str(self.pop[-1].getIDs()))
    
        bestout.write('Best Camera Set:\n' + str(self.pop[-1]))
        bestout.write('\nSighted by Best:\n'+ str(self.pop[-1].getIDs()) + '\n')
        bestout.write('\nBestFitness:\n' + str(self.pop[-1].getFitness())) 
                
        print('\n\nBest Camera Set:\n' + str(self.pop[-1]))
        print('\nSighted by Best:\n'+ str(self.pop[-1].getIDs()) + '\n')
        print('\nBest Fitness:\n' + str(self.pop[-1].getFitness()) + '\n') 
    
    def tournament_selection (self, n, k):
        inds = random.sample(self.pop, n)
        inds.sort()
        return inds[-k:]
     
    def fps (self):
        totalScore = 0
        for i in self.pop:
            totalScore += i.fitness

        selected = random.randint(0, int(totalScore))

        selectedInd = -1
        curScore = 0
        for i in range(0, len(self.pop)):
            curScore += self.pop[i].fitness
            if selected <= curScore:
                selectedInd = i
                break
        ind = self.pop[selectedInd]
        return (ind)
    
class Individual (object):
    def __init__ (self, aWorld, camCount=1, camRad = 1, \
                  fitFunc="getSightingsMade", sightings = []):
        """ An individual consists of a set of cameras"""
        self.fitness = -1
        self.fitFunc = fitFunc
        self.sightings = sightings
        self.camCount = camCount
        self.camRadius = camRad
        self.world = aWorld
        self.animalsSeen = None
        self.mySightings = None
        self.cameras = []
        self.randCameras()
        self.lenAnimalSightings = 0

    def getFitness(self):
        return self.fitness

    def randCameras (self):
        """ Initialize a set of cameras to random locations """
        for i in range (0, self.camCount):
            loc = self.world.randLoc()
            self.cameras.append(camera.Camera(loc,self.camRadius))
        self.evalFitness()

    def setCameras(self, cameras):
        """ Place cameras for testing purposes"""
        if (self.camCount != len(cameras)):
            raise AssertionError ("Wrong number of cameras")
        badCam = [c for c in cameras if (self.world.locationInWorld(c.loc) == False)]
        if (len(badCam) > 0):
            raise AssertionError ("Bad camera location")
        self.cameras = cameras
        self.reset()
        self.evalFitness()

    def crossover (self, other):
        pointOne = random.randint(0, len(self.cameras))    
        pointTwo = random.randint(0, len(self.cameras))
        while (pointOne == pointTwo):
            pointTwo = random.randint(0, len(self.cameras))

        if pointOne > pointTwo:
            pointOne, pointTwo = pointTwo, pointOne

        progOneCameras = self.cameras[:pointOne] + other.cameras[pointOne:pointTwo] +\
                  self.cameras[pointTwo:]
        progTwoCameras = other.cameras[:pointOne] + self.cameras[pointOne:pointTwo] +\
                  other.cameras[pointTwo:]

        progOne = Individual(self.world, self.camCount, self.camRadius, self.fitFunc, self.sightings)
        progOne.setCameras(progOneCameras)
        progTwo = Individual(self.world, self.camCount, self.camRadius, self.fitFunc, self.sightings)
        progTwo.setCameras(progTwoCameras)
        return progOne, progTwo

    def mutate (self, mut_rate):
        for i in range (0, len(self.cameras)):
            rand = random.uniform(0, 1)
            if rand < mut_rate:
                loc = self.world.randLoc()
                self.cameras[i] = camera.Camera(loc,self.camRadius)
        self.reset()
        self.evalFitness()

    def __str__(self):
        myStr = ""
        for c in self.cameras:
            myStr += str(c)
            myCurrSightings = []
            for s in self.sightings:
                if (c.makesSighting(s)):
                    if (s.getAnimalID() not in myCurrSightings):
                        myCurrSightings.append(s.getAnimalID())
            if (len(myCurrSightings) > 0): 
                myStr += ', ' + str(myCurrSightings)
            myStr += '\n'
        return myStr        

    def __lt__(self, other):
        return self.fitness < other.fitness

    def reset (self):
        self.fitness = -1
        self.animalsSeen = None
        self.mySightings = None

    def evalFitness (self):
        if (self.mySightings == None):
            self.observedSightings()
        self.fitness = (getattr(self, self.fitFunc)())
        return self.fitness

    def observedSightings(self):
        mySightings = []
        for c in self.cameras:
            mySightings += [s for s in self.sightings if c.makesSighting(s)]
        self.mySightings = list(set(mySightings))

    def getAnimalsSeen(self):
        self.animalsSeen = list(set([s.getAnimalID() for s in self.mySightings]))
        return len(self.animalsSeen)
#        return self.calcDistFitness()

    def calcDistFitness(self):
        for c in self.cameras:
            for s in self.sightings:
                myDistFitness += c.distSighting(s)
        return myDistFitness

    def getSightingsMade(self):
        return len(self.mySightings)

    def getIDs(self):
        self.animalsSeen = list(set([s.getAnimalID() for s in self.mySightings]))
        return self.animalsSeen

    def getTotalAnimalRange(self):
        myAnimalSightings = {}
        for c in self.cameras:
            for s in self.sightings:
                if (c.makesSighting(s)):
                    if (s.getAnimalID() not in myAnimalSightings):
                        myAnimalSightings[s.getAnimalID()] = []
                    # For this, we append the four corner coordinates of the
                    # camera. This handles the case where only one or two
                    # cameras see an animal.
                    myAnimalSightings[s.getAnimalID()].append((c.getLowX(), c.getLowY()))
                    myAnimalSightings[s.getAnimalID()].append((c.getLowX(), c.getUpperY()))
                    myAnimalSightings[s.getAnimalID()].append((c.getUpperX(), c.getLowY()))
                    myAnimalSightings[s.getAnimalID()].append((c.getUpperX(), c.getUpperY()))

        conhull = convexHull.CH()
        rangeSize = 0.0
        for a in myAnimalSightings:
            cHullPts = conhull.convexHull(myAnimalSightings[a])
            # Currently does not handle the case where 1 or 2 cameras
            # spotted an animal.
            rangeSize += conhull.polygon_area(cHullPts)
        self.lenAnimalSightings = len(myAnimalSightings)
        return rangeSize

    def getProductAnimalRanges(self):
        rSize = self.getTotalAnimalRange()
        numAnimals = self.lenAnimalSightings
        return (rSize * numAnimals)
