import ConfigParser
import math
import random
from optparse import OptionParser


def main():
    config = ConfigParser.ConfigParser()
    config.read('placeControlCams.ini')

    parser = OptionParser()
    parser.add_option('-o', help='outputFile', type="string", nargs=1, dest="outputFile")
    parser.add_option('-s', help='scenario', type="int", nargs=1, dest="scenario")

    (options, args) = parser.parse_args()
    
    scenario = int(config.get('SCENARIO', 'scenario', 0))
    if (options.scenario != None): scenario = options.scenario

    maxCameras = float(config.get('SCENARIO', 'maxCameras', 0))

    minNorthing = float(config.get('SCENARIO', 'minNorthing', 0))
    minEasting = float(config.get('SCENARIO', 'minEasting', 0))
    maxNorthing = float(config.get('SCENARIO', 'maxNorthing', 0))
    maxEasting = float(config.get('SCENARIO', 'maxEasting', 0))
    
    randSeed = int(config.get('SCENARIO', 'randSeed', -1))
    if (randSeed == -1):
        randSeed = None
    random.seed(randSeed)

    camRadius = int(config.get('SCENARIO', 'camRadius', 0))
            
    mu = int(config.get('SCENARIO', 'stdDev', 10))

    orgs = config.get('SCENARIO', 'orgList', "F101,F102,M103,F104,F105,F108,F110,M114,M115,F116")
    orgList = orgs.split(',')
    locFile = config.get('SCENARIO', 'locFile', '../fieldData/hyenaData/allOrgs.dat')
    outfile = config.get('OUTPUT', 'outputFile', 'controlData.dat')
            
    if (options.outputFile != None): outfile = options.outputFile
    
    if scenario == 0 or scenario == 1:
        x_list, y_list = makeGrid(maxCameras, minEasting, maxEasting, minNorthing, maxNorthing, scenario, camRadius)
        printMultList(outfile, x_list, y_list)
    elif scenario == 2:
        x_list, y_list = placeRandom(maxCameras, minEasting, maxEasting, minNorthing, maxNorthing, camRadius)
        printList(outfile, x_list, y_list, 0)
    elif scenario == 3:
        x_list, y_list, num_rand = getOppSightings(maxCameras, minEasting, maxEasting, minNorthing, maxNorthing, orgList, locFile, mu, camRadius)
        printList(outfile, x_list, y_list, num_rand)
        
def makeGrid(maxCameras, minEasting, maxEasting, minNorthing, maxNorthing, scenario, camRadius):
    east_dist = maxEasting - minEasting
    north_dist = maxNorthing - minNorthing

    x_y_ratio = east_dist / north_dist
    y_x_ratio = north_dist / east_dist

    xideal_blocks = math.sqrt(maxCameras) * x_y_ratio
    yideal_blocks = math.sqrt(maxCameras) * y_x_ratio
    numidealblocks = xideal_blocks * yideal_blocks

    maxRealBlocks = maxCameras + min(maxCameras + (math.floor(xideal_blocks) * math.ceil(yideal_blocks)), maxCameras + (math.ceil(xideal_blocks) * math.floor(yideal_blocks)))

    xblocks = math.ceil(xideal_blocks)
    if maxRealBlocks % math.ceil(xideal_blocks):
        xblocks = math.floor(xideal_blocks)

    yblocks = math.ceil(yideal_blocks)
    if maxRealBlocks % math.ceil(yideal_blocks):
        yblocks = math.floor(yideal_blocks)

    xblock_size = east_dist / xblocks
    yblock_size = north_dist / yblocks

    if (scenario == 0):
        x_list, y_list = blockCenters(xblocks, yblocks, minEasting, minNorthing, xblock_size, yblock_size)
    elif (scenario == 1):
        x_list, y_list = randomStratified(xblocks, yblocks, minEasting, minNorthing, xblock_size, yblock_size, camRadius)

    return x_list, y_list

def blockCenters(xblocks, yblocks, minEasting, minNorthing, xblock_size, yblock_size):
    x_edge_offset = xblock_size / 2.0
    y_edge_offset = yblock_size / 2.0

    x_list = []
    x_list.append(minEasting + x_edge_offset)
    y_list = []
    y_list.append(minNorthing + y_edge_offset)
    
    while len(x_list) < xblocks:
        x_list.append(x_list[-1] + xblock_size)
    while len(y_list) < yblocks:
        y_list.append(y_list[-1] + yblock_size)
                      
    return x_list, y_list

def randomStratified(xblocks, yblocks, minEasting, minNorthing, xblock_size, yblock_size, camRadius):
    next_low_x = minEasting + camRadius  
    next_low_y = minNorthing + camRadius

    x_list = []
    x_list.append(random.randint(next_low_x, next_low_x + xblock_size - 2 * camRadius))
    y_list = []
    y_list.append(random.randint(next_low_y, next_low_y + yblock_size - 2 * camRadius))
        
    while len(x_list) < xblocks:
        next_low_x += xblock_size
        x_list.append(random.randint(next_low_x, next_low_x + xblock_size - 2 * camRadius))
    while len(y_list) < yblocks:
        next_low_y += yblock_size
        y_list.append(random.randint(next_low_y, next_low_y + yblock_size - 2 * camRadius))
    
    return x_list, y_list

def placeRandom(maxCameras, minEasting, maxEasting, minNorthing, maxNorthing, camRadius):
    low_x = minEasting + camRadius
    hi_x = maxEasting - camRadius
    low_y = minNorthing + camRadius
    hi_y = maxNorthing - camRadius

    x_list = []
    y_list = []
    while len(x_list) < maxCameras:
        x_num = random.randint(low_x, hi_x)
        y_num = random.randint(low_y, hi_y)
        
        validCam = True
        if len(x_list) > 0:
            index = 0
            for x_val in x_list:
                x_dist = x_num - x_val
                y_dist = y_num - y_list[index]
                index += 1
                
                offset = math.sqrt(float(x_dist * x_dist) + float(y_dist * y_dist)) 
                if offset < camRadius:
                    validCam = False
        if validCam:
            x_list.append(x_num)
            y_list.append(y_num)
    
    return x_list, y_list

def getOppSightings(maxCameras, minEasting, maxEasting, minNorthing, maxNorthing, orgList, locFile, mu, camRadius):
    sightings = []
    f = open(locFile)
    fileData = f.read()
    f.close()
    
    if '\r' in fileData:
        data = fileData.split('\r')
    else:
        data = fileData.split('\n')
        # get rid of hanging spaces and hanging newline at end of file
        data = [l.strip() for l in data][:-1]    

    # build list of valid coordinates 
    x_locs = []
    y_locs = []
    for line in data:
        splitdata = line.split(',')
        if splitdata[0] not in orgList:
            continue
        elif int(splitdata[1]) < minEasting or int(splitdata[1]) > maxEasting:
            continue
        elif int(splitdata[2]) < minNorthing or int(splitdata[2]) > maxNorthing:
            continue
        else:
            x_locs.append(splitdata[1].strip())
            y_locs.append(splitdata[2].strip())

    num_sightings = abs(int(random.gauss(0, mu)))
    if num_sightings > maxCameras:
        num_sightings = maxCameras
    if num_sightings > len(x_locs):
        num_sightings = len(x_locs)
    targets = random.sample(xrange(len(x_locs)), num_sightings)    

    x_list = []
    y_list = []
    for target in targets:
        x_list.append(x_locs[target])
        y_list.append(y_locs[target])

    numRandCameras = maxCameras - len(x_list)
    x_list, y_list = fillRandom(maxCameras, minEasting, maxEasting, minNorthing, maxNorthing, camRadius, x_list, y_list)
    return x_list, y_list, numRandCameras

def fillRandom(maxCameras, minEasting, maxEasting, minNorthing, maxNorthing, camRadius, x_list, y_list):
    low_x = minEasting + camRadius
    hi_x = maxEasting - camRadius
    low_y = minNorthing + camRadius
    hi_y = maxNorthing - camRadius
    
    while len(x_list) < maxCameras:
        x_num = random.randint(low_x, hi_x)
        y_num = random.randint(low_y, hi_y)
        
        validCam = True
        if len(x_list) > 0:
            index = 0
            for x_val in x_list:
                x_dist = x_num - int(x_val)
                y_dist = y_num - int(y_list[index])
                index += 1
                
                offset = math.sqrt(float(x_dist * x_dist) + float(y_dist * y_dist)) 
                if offset < camRadius:
                    validCam = False
        if validCam:
            x_list.append(x_num)
            y_list.append(y_num)
    
    return x_list, y_list

def printMultList(outfile, x_list, y_list):
    output = open(outfile, 'w')
    print('Actual number of control cameras to place = ' + str(len(x_list) * len(y_list)) + '\n')
    for x in x_list:
        for y in y_list:
            output.write(str(x) + ', ' + str(y) + '\n')
            print(str(x) + ', ' + str(y))

def printList(outfile, x_list, y_list, num_rand):
    output = open(outfile, 'w')
    print('Number of control cameras to place = ' + str(len(x_list)) + '\n')
    if num_rand > 0:
        tmpCount = len(x_list) - num_rand
        print('(' + str(tmpCount) + ' opportunistic sightings and ' + str(num_rand) + ' placed randomly)\n')
    index = 0
    for x in x_list:
        output.write(str(x) + ', ' + str(y_list[index]) + '\n')
        print(str(x) + ', ' + str(y_list[index]))
        index += 1

if __name__ == "__main__":
    main()

