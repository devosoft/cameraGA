import ConfigParser
from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option('-s', help='starting week', type="int", nargs=1, dest="start")
    parser.add_option('-e',help='ending week (-1 for last week of data', type="int", nargs=1, dest="end")
    parser.add_option('-o',help='output file', type="string", nargs=1, dest="outputFile")
    parser.add_option('-i', help='increment; 0=all data', type="int", nargs=1, dest='inc')
                      
    (options, args) = parser.parse_args()

    config = ConfigParser.ConfigParser()
    config.read('getFieldData.ini')
    
    orgs = config.get('ORGS', 'orgList', "F101,F102,M103,F104,F105,F108,F110,M114,M115,F116")
    orgList = orgs.split(',')
        
    locFile = config.get('ORGS','fieldFile', 'origData/allShompoleLOCs.csv')
    firstWeek = int(config.get('ORGS','firstWeek', 0))
    if (options.start != None): firstWeek = options.start
    lastWeek = int(config.get('ORGS','lastWeek', -1))
    if (options.end != None): lastWeek = options.end
    outputFile = config.get('OUTPUTS','outputFile', 'orgs.dat')
    if (options.outputFile != None): outputFile=options.outputFile
                      
    increment = int(config.get('ORGS','increment', 0))
    if (options.inc != None): increment=options.inc

    if (increment == 0):
        locData = readLocFile(locFile, orgList, firstWeek, lastWeek)
        printResults(outputFile, locData)
    else:
        curFirst = firstWeek
        curLast = firstWeek + (increment - 1) # the -1 is to account for the fact the data is
                                                # in 1 week increments
        while (curLast <= lastWeek):
            locData = readLocFile(locFile, orgList, curFirst, curLast)
            longOut = outputFile + "_" + str(curFirst)+"_"+str(curLast)
            printResults(longOut, locData)
            curFirst += increment 
            curLast += increment 

def readLocFile(filename, orgList, firstWeek, lastWeek):
    sightings = []
    f = open(filename)
    fileData = f.read()
    f.close()
    if '\r' in fileData:
        data = fileData.split('\r')
    else:
        data = fileData.split('\n')
    # get rid of hanging spaces 
    data = [l.strip() for l in data]    
    
    sightings.append(data[0].split(','))
    for line in data:
        splitline = line.split(',')
        if splitline[0] in orgList and int(splitline[-2]) >= firstWeek and (int(splitline[-2]) <= lastWeek or lastWeek == -1):
            sightings.append(splitline)
    return sightings        


def printResults(outfile, locData):
    output = open(outfile, 'w')
    for line in locData:
        linestr = ""
        for item in line[:-1]:
            linestr += (item + ', ')
        linestr += line[-1]
        output.write(linestr + '\n')


if __name__ == "__main__":
    main()

