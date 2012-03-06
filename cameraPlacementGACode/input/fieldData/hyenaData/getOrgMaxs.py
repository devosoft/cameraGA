def main():
    outfile = 'F101-F108Maxs.dat'
    locData = readLocFile('F101-F108.dat', outfile)

def readLocFile(infile, outfile):
    sightings = []
    f = open(infile)
    fileData = f.read()
    f.close()
    
    output = open(outfile, 'w')
    
    if '\r' in fileData:
        data = fileData.split('\r')
    else:
        data = fileData.split('\n')
    # get rid of hanging spaces and hanging newline at end of file
        data = [l.strip() for l in data][:-1]    
    
    # handle first org in file
    org = data[1].split(',')[0]
    globmaxEast = globminEast = maxEast = minEast = int(data[1].split(',')[1])
    globmaxNorth = globminNorth = maxNorth = minNorth = int(data[1].split(',')[2])
    maxweek = 0

    for line in data[1:]:
        splitline = line.split(',')
        if org == str(splitline[0]):
            maxweek = splitline[-2]
            if int(splitline[1]) < minEast:
                minEast = int(splitline[1])
            if int(splitline[1]) > maxEast:
                maxEast = int(splitline[1])
            if int(splitline[2]) < minNorth:
                minNorth = int(splitline[2])
            if int(splitline[2]) > maxNorth:
                maxNorth = int(splitline[2])
        
        if org != str(splitline[0]):
            if minEast < globminEast:
                globminEast = minEast
            if maxEast > globmaxEast:
                globmaxEast = maxEast
            if minNorth < globminNorth:
                globminNorth = minNorth
            if maxNorth > globmaxNorth:
                globmaxNorth = maxNorth
            print(org + ':' + '\n' + ' last week ' + str(maxweek) + '\n' + 
                  ' Easting (min max): ' + str(minEast) + ' ' + str(maxEast) + '\n' + 
                  ' Northing (min max): ' + str(minNorth) + ' ' + str(maxNorth) + '\n') 
            output.write(org + ':' + '\n' + ' last week ' + str(maxweek) + '\n' + 
                  ' Easting (min max): ' + str(minEast) + ' ' + str(maxEast) + '\n' + 
                  ' Northing (min max): ' + str(minNorth) + ' ' + str(maxNorth) + '\n') 
            org = str(splitline[0])
            minEast = maxEast = int(splitline[1])
            minNorth = maxNorth = int(splitline[2])

    # handle last org in file
    print(org + ':' + '\n' + ' last week ' + str(maxweek) + '\n' + 
          ' Easting (min max): ' + str(minEast) + ' ' + str(maxEast) + '\n' + 
          ' Northing (min max): ' + str(minNorth) + ' ' + str(maxNorth) + '\n') 
    output.write(org + ':' + '\n' + ' last week ' + str(maxweek) + '\n' + 
          ' Easting (min max): ' + str(minEast) + ' ' + str(maxEast) + '\n' + 
          ' Northing (min max): ' + str(minNorth) + ' ' + str(maxNorth) + '\n')         
                
    if minEast < globminEast:
        globminEast = minEast
    if maxEast > globmaxEast:
        globmaxEast = maxEast
    if minNorth < globminNorth:
        globminNorth = minNorth
    if maxNorth > globmaxNorth:
        globmaxNorth = maxNorth

    print('Global Easting (min max): ' + str(globminEast) + ' ' + str(globmaxEast) + '\n' + 
          'Global Northing (min max): ' + str(globminNorth) + ' ' + str(globmaxNorth) + '\n') 
    output.write('\nGlobal Easting (min max): ' + str(globminEast) + ' ' + str(globmaxEast) + '\n' + 
          'Global Northing (min max): ' + str(globminNorth) + ' ' + str(globmaxNorth) + '\n') 
     

if __name__ == "__main__":
    main()

