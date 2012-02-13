import world
import camera
import sighting
import ga
import unittest
import random
import convexHull

""" Unit test for camera placement GA"""

class LocationWorldTest (unittest.TestCase):
    def testLocationCreation(self):
        l = world.Location(0,0)
        self.assertEqual(l.getX(), 0)
        self.assertEqual(l.getY(), 0)
        
    def testLocationInWorldSuccess(self):
        w = world.World(0,10,0,10)
        self.assertEqual(w.inWorld(1,1), True)
        
    def testLocationInWorldFail(self):
        w = world.World(0,10,0,10)
        self.assertEqual(w.inWorld(-1,-1), False)

class SightingTest (unittest.TestCase):
    def testCameraCanSeeSuccess (self):
        l = world.Location(0,0)
        l2 = world.Location(2,2)
        c = camera.Camera(l, 5)
        self.assertEqual(c.canSee(l2), True)

    def testCameraCanSeeFail (self):
        l = world.Location(0,0)
        l2 = world.Location(6,6)
        c = camera.Camera(l, 5)
        self.assertEqual(c.canSee(l2), False)

    def testCameraMakesSightingSuccess (self):
        l = world.Location(0,0)
        l2 = world.Location(3,3)
        s = sighting.Sighting(l2, "george")
        c = camera.Camera(l, 5)
        self.assertEqual(c.makesSighting(s), True)
        
    def testCameraMakesSightingFail (self):
        l = world.Location(0,0)
        l2 = world.Location(7,7)
        s = sighting.Sighting(l2, "paul")
        c = camera.Camera(l, 5)
        self.assertEqual(c.makesSighting(s), False)

class IndividualTest (unittest.TestCase):
    
    def testMutateNoMutations (self):
        w = world.World(0,10,0,10)
        i = ga.Individual(w, camCount=2, camRad=2)
        c1 = camera.Camera(world.Location(0, 0), 2)
        c2 = camera.Camera(world.Location(10, 10), 2)
        i.setCameras([c1,c2])
        i.mutate(0)
        self.assertEqual([c1,c2] == i.cameras, True)

    def testMutateSomeMutations (self):
        w = world.World(0,10,0,10)
        i = ga.Individual(w, camCount=2, camRad=2)
        c1 = camera.Camera(world.Location(0, 0), 2)
        c2 = camera.Camera(world.Location(10, 10), 2)
        i.setCameras([c1,c2])
        i.mutate(1)
        self.assertEqual([c1,c2] != i.cameras, True)

    def testSightings (self):
        # create sightings
        s1 = sighting.Sighting(world.Location(0,0), "john")
        s2 = sighting.Sighting(world.Location(3,3), "paul")
        s3 = sighting.Sighting(world.Location(6,6), "george")
        s4 = sighting.Sighting(world.Location(9,9), "ringo")
        s = [s1,s2,s3,s4]
        
        # create a world with two cameras with radius 2
        w = world.World(0,10,0,10)
        i = ga.Individual(w, camCount=2, camRad=2, sightings=s)
        c1 = camera.Camera(world.Location(0, 0), 2)
        c2 = camera.Camera(world.Location(10, 10), 2)
        i.setCameras([c1,c2])

        i.observedSightings()
        self.assertEqual((2) == i.getAnimalsSeen(), True)
        self.assertEqual(2 == (i.evalFitness()), True)

    def testGetRange (self):
        # create sightings
        s1 = sighting.Sighting(world.Location(0,0), "john")
        s2 = sighting.Sighting(world.Location(10,10), "john")
        s3 = sighting.Sighting(world.Location(2,2), "ringo")
        s4 = sighting.Sighting(world.Location(9,9), "ringo")
        s5 = sighting.Sighting(world.Location(1,9), "ringo")
        s = [s1,s2,s3,s4,s5]
        
        # create a world with two cameras with radius 2
        w = world.World(0,10,0,10)
        i = ga.Individual(w, camCount=3, camRad=2, sightings=s)
        c1 = camera.Camera(world.Location(0, 0), 2)
        c2 = camera.Camera(world.Location(10, 10), 2)
        c3 = camera.Camera(world.Location(0, 10), 2)

        i.setCameras([c1,c2,c3])

        i.observedSightings()
        print (i.getRanges())
        self.assertEqual(242.0 == i.getRanges(), True)

    def testEvalFitnessAfterMutations (self):
        # check that eval fitness changes after mutations
        random.seed(1)
        s1 = sighting.Sighting(world.Location(0,0), "john")
        s2 = sighting.Sighting(world.Location(10,10), "john")
        s3 = sighting.Sighting(world.Location(2,2), "ringo")
        s4 = sighting.Sighting(world.Location(9,9), "ringo")
        s5 = sighting.Sighting(world.Location(1,9), "ringo")
        s = [s1,s2,s3,s4,s5]
        w = world.World(0,10,0,10)
        i = ga.Individual(w, camCount=2, camRad=2, sightings=s)
        c1 = camera.Camera(world.Location(0, 0), 2)
        c2 = camera.Camera(world.Location(10, 10), 2)
        i.setCameras([c1,c2])
        i.evalFitness()
        self.assertEqual(i.fitness == 4, True)
        i.mutate(100)
        self.assertEqual(i.fitness == 2, True)


    def testEvalFitnessAfterCrossover (self):
        # check that eval fitness changes after crossover
        random.seed(1)
        s1 = sighting.Sighting(world.Location(0,0), "john")
        s2 = sighting.Sighting(world.Location(10,10), "john")
        s3 = sighting.Sighting(world.Location(2,2), "ringo")
        s4 = sighting.Sighting(world.Location(9,9), "ringo")
        s5 = sighting.Sighting(world.Location(1,9), "ringo")
        s = [s1,s2,s3,s4,s5]
        w = world.World(0,10,0,10)

        # ind 1
        i = ga.Individual(w, camCount=2, camRad=2, sightings=s)
        c1 = camera.Camera(world.Location(0, 0), 2)
        c2 = camera.Camera(world.Location(10, 10), 2)
        i.setCameras([c1,c2])
        i.evalFitness()
        self.assertEqual(i.fitness == 4, True)

        # ind 2
        i2 = ga.Individual(w, camCount=2, camRad=2, sightings=s)
        c1 = camera.Camera(world.Location(5, 5), 2)
        c2 = camera.Camera(world.Location(6, 6), 2)
        i2.setCameras([c1,c2])
        i2.evalFitness()
        self.assertEqual(i2.fitness == 0, True)

        p1, p2 = i.crossover(i2)
        self.assertEqual(p1.fitness == 2, True)
        self.assertEqual(p2.fitness == 2, True)

        
class ConvexHullTest (unittest.TestCase):
    def testTriangle (self):
        p = [(0,20), (0,0), (10,10)]
        conHull = convexHull.CH()
        op = conHull.convexHull(p)
        self.assertEqual(op, [(0,0), (0,20), (10,10)], True)
        area = conHull.polygon_area(op)
        self.assertEqual(area, 100, True)

    def testSquare (self):
        p = [(0,20), (0,0), (20,20), (20,0)]
        conHull = convexHull.CH()
        op = conHull.convexHull(p)
        self.assertEqual(op, [(0,0), (0,20), (20,20), (20,0)], True)
        area = conHull.polygon_area(op)
        self.assertEqual(area, 400, True)

class GATest (unittest.TestCase):
    def testRandNumGeneratorConsistency(self):
        seed = 1
        random.seed(1)
        myGA1 = ga.GA(2, 1, 0, 0, "getSightingsMade")
        w = world.World(0,10,0,10)
        myGA1.initPop(w, 1, 1, [])
        coord1 = (str(myGA1.pop[0].cameras[0]))

        random.seed(1)
        myGA2 = ga.GA(2, 1, 0, 0, "getSightingsMade")
        w2 = world.World(0,10,0,10)
        myGA2.initPop(w, 1, 1, [])        
        coord2 = (str(myGA2.pop[0].cameras[0]))

        random.seed(2)
        myGA3= ga.GA(2, 1, 0, 0, "getSightingsMade")
        w3 = world.World(0,10,0,10)
        myGA3.initPop(w, 1, 1, [])        
        coord3 = (str(myGA3.pop[0].cameras[0]))
        
        self.assertEqual(coord1 == coord2, True)
        self.assertEqual(coord1 != coord3, True)
        

if __name__ == "__main__":
    unittest.main()
    
