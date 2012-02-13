import ConfigParser

def main():
    config = ConfigParser.ConfigParser()
    config.read('getFieldData.ini')
    
    orgs = config.get('ORGS', 'orgList', "F101,F102,M103,F104,F105,F108,F110,M114,M115,F116")
    orgList = orgs.split(',')
        
    locFile = config.get('ORGS','fieldFile', 'origData/allShompoleLOCs.csv')
    firstWeek = int(config.get('ORGS','firstWeek', 0))
    lastWeek = int(config.get('ORGS','lastWeek', -1))
    locData = readLocFile(locFile, orgList, firstWeek, lastWeek)
                    
    printResults(config.get('OUTPUTS','outputFile', 'orgs.dat'), locData)


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

