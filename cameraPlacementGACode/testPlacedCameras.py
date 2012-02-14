import world
import camera
import sighting
import ga
import unittest
import random
import convexHull
import configparser
import argparse
import csv

def main():

    config = configparser.ConfigParser()
    config.read('hyena.ini')

    parser = argparse.ArgumentParser(description='Process command line.')
    parser.add_argument('-camFile', 
                   help='list of camera locations')
    parser.add_argument('-trainSightingsData', 
                   help='list of train animal sightings')
    parser.add_argument('-testSightingsData', 
                   help='list of test animal sightings')
    parser.add_argument('-analysisOutFile', 
                   help='file for analysis output')
    
    args = parser.parse_args()
    print(args)
    
    
    ### Create the world
    thisWorld = config['LOCATION']
    try:
        lowX = float(thisWorld.get('lowerx', 0))
        upX = float(thisWorld.get('upperx', 10))
        lowY = float(thisWorld.get('lowery', 0))
        upY = float(thisWorld.get('uppery', 10))
    except ValueError:
        print ("Invalid x,y coordinates for location")
        exit()

    w = world.World(lowX,upX,lowY,upY)


    ### Load sightings
    trainsightingsData = config['SIGHTINGS_DATA'].get('datafile', 'sightings.dat')
    if (args.trainSightingsData != None):
        trainsightingsData = args.trainSightingsData
    trainsightings = readSightingsFile(trainsightingsData, w)

    ### Get equipment settings
    thisEquip = config['CAMERA_SPECS']
    try:
        numCameras = int(thisEquip.get('numCameras', 50))
        visibilityRadius = float(thisEquip.get('visibilityRadius', 5))

    except ValueError:
        print ("Invalid camera specification parameters")
        exit()

    ### Get settings for perfomance evalution
    testsightingsData = config['PERFORMANCE_EVALUATION'].get('testingDatafile', 'sightings.dat')
    if (args.testSightingsData != None):
        testsightingsData = args.testSightingsData
    testsightings = readSightingsFile(testsightingsData, w)
    thisEquip = config['PERFORMANCE_EVALUATION']
    try:
        equipFile=thisEquip.get('cameraFile', 'best.dat')
        if (args.camFile != None):
            equipFile = args.camFile
        analysisOutFile=thisEquip.get('analysisOutFile', 'analysis.dat')
        if (args.analysisOutFile != None):
            analysisOutFile = args.analysisOutFile

    except ValueError:
      print ("Invalid performance evaluation parameters")
      exit()

    thisGA = config['GA_SETTINGS']
    try:
        fitnessFunction = int(thisGA.get("fitnessFunction", 0))
        if ((fitnessFunction < 0) or (fitnessFunction > 3)):
            print ("Invalid fitness function")
            exit()
        if (fitnessFunction == 0):
            fitFuncName = "getSightingsMade"
        elif (fitnessFunction == 1):
            fitFuncName = "getAnimalsSeen"
        elif (fitnessFunction == 2):
            fitFuncName = "getTotalAnimalRange"
        elif (fitnessFunction == 3):
            fitFuncName = "getProductAnimalRanges"
    except ValueError:
        print ("Invalid value for GA settings")
        exit()
            
    ### Get the set of cameras from the file.
    f = open(equipFile, 'r')
    fout = open(analysisOutFile, 'w')

    cameras = []
    for line in f:
        if (line[0].isdigit()):
            splitline = line.split(",")
            coorx = float(splitline[0])
            coory = float(splitline[1])
            cameras.append(camera.Camera(world.Location(coorx, coory), visibilityRadius))
    i2 = ga.Individual(w, camCount=numCameras, camRad=visibilityRadius, fitFunc=fitFuncName, sightings=trainsightings)
    i2.setCameras(cameras)
    train = str(i2.evalFitness())
    i2ids = str(i2.getIDs())
    i3 = ga.Individual(w, camCount=numCameras, camRad=visibilityRadius, fitFunc=fitFuncName, sightings=testsightings)
    i3.setCameras(cameras)
    test = str(i3.evalFitness())
    i3ids = str(i3.getIDs())
    s = "SUMMARY" + "\n" + "Training data fitness: " + train + ' ' + i2ids + "\n" + "Testing data fitness: " + test + ' ' + i3ids + "\n\n" + "TRAINING RESULTS" + "\n" + str(i2) + "\n" + "TESTING RESULTS" + "\n" + str(i3) + "\n"
    fout.write(s)
    print("\n" + s)
    print("obs: ")
    i3.observedSightings()

def readSightingsFile(filename, w):
    sightingsReader = csv.reader(open(filename))
    sightings = []
    # skip header line
    sightingsReader.__next__()
    for row in sightingsReader:
        try: 
            loc = world.Location(float(row[1]), float(row[2]))
        except ValueError:
            print ("Invalid x,y coordinates for location", row[1], row[2])
            continue
        if (w.locationInWorld(loc)): 
            sightings.append(sighting.Sighting(loc, row[0]))
        else:
            print ("Input sighting outside of defined world: ", loc.getX(), " ", loc.getY())
    return sightings        


if __name__ == "__main__":
    main()
