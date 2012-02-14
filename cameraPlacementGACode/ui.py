import configparser
import argparse
import csv
import world
import sighting
import ga
import random


def main():
    config = configparser.ConfigParser()
    config.read('hyena.ini')

    parser = argparse.ArgumentParser(description='Process command line.')
    parser.add_argument('-s',
                   help='random number seed')
    parser.add_argument('-runOutput', 
                   help='run log output file')
    parser.add_argument('-bestOutput', 
                   help='best of run output file')
    parser.add_argument('-sightingsData', 
                   help='list of animal sightings')
    
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
    sightingsData = config['SIGHTINGS_DATA'].get('datafile', 'sightings.dat')
    if(args.sightingsData != None):
        sightingsData = args.sightingsData
        print ("Overriding sightings data...")
    sightings = readSightingsFile(sightingsData, w)

    ### Get equipment settings
    thisEquip = config['CAMERA_SPECS']
    try:
        numCameras = int(thisEquip.get('numCameras', 50))
        visibilityRadius = float(thisEquip.get('visibilityRadius', 5))
    except ValueError:
        print ("Invalid equipment parameters")
        exit()


    ### Create the GA
    thisGA = config['GA_SETTINGS']
    ### Initialize random number generator
    try:
      randSeed = int(config['GA_SETTINGS'].get('randNumberSeed', -1))
      if(args.s != None):
        randSeed = int(args.s)
        print (randSeed)
    except ValueError:
      print ("Invalid value for random number seed")
      exit()

    if (randSeed == -1):
      randSeed = None
    random.seed(randSeed)
    ### Select fitness function parameters and type
    try:
        popSize = int(thisGA.get("populationSize", 100))
        gen = int(thisGA.get("generations", 100))
        selection = int(thisGA.get("selection", 0))
        if ((selection < 0) or (selection > 1)):
            print ("Invalid selection strategy")
            exit()
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
            
        crossPer = float(thisGA.get("crossoverPer", 0))
        if ((crossPer < 0) or (crossPer > 1)):
            print ("Invalid crossover percentage")
            exit()
        mutPer = float(thisGA.get("mutationPer", 0))
        if ((mutPer < 0) or (mutPer > 1)):
            print ("Invalid mutation probability")
            exit()
        runOutputFile = str(thisGA.get("runOutputFile", "run.log"))
        bestOutputFile = str(thisGA.get("bestOutputFile", "best.dat"))
        if(args.runOutput != None):
            runOutputFile = str(args.runOutput)
            print (runOutputFile)
        if(args.bestOutput != None):
            bestOutputFile = str(args.bestOutput)
            print (bestOutputFile)
    except ValueError:
        print ("Invalid value for GA settings")
        exit()

    ### Run the GA
    g = ga.GA(gen, popSize, crossPer, mutPer, fitFuncName, selection, runOutputFile, bestOutputFile)
    g.initPop(w, numCameras, visibilityRadius, sightings)
    g.run()
    

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

