import ConfigParser
from pylab import *

def main():
    config = ConfigParser.ConfigParser()
    config.read('map.ini')
    
    ### Load file with GA 'hits' and actual org sightings files
    gaHitsData = config.get('PLOT_DATA','plotDatafile', 'best.dat')
    gaHits = readHitsFile(gaHitsData)
    sightingsData = config.get('PLOT_DATA', 'orgLocfile', 'sightings.dat')
    sightings = readSightingsFile(sightingsData)
          
    ### Need to draw polygons?
    drawRanges = config.get('PLOT_DATA', 'isRangeData', 0)
    if (not drawRanges.isdigit() or int(drawRanges) < 0 or int(drawRanges) > 1): 
        print ("Invalid entry for isRangedata")
        exit()
  
    plotType = "scatter"
    if (int(drawRanges) == 1):
        plotType = "ranges"
    plotResults(config.get('OUTPUTS','plotOutputfile', 'plot.dat'), gaHits, plotType, sightings)

def readHitsFile(filename):
    sightings = []
    f = open(filename)
    fileData = f.read()
    f.close()
    data = fileData.split('\n')
    # get rid of hanging spaces and the hanging new line at end of file
    data = [l.strip() for l in data][:-1]    
  
    is_test_dat = False
    found_test_dat = False
    for line in data:
        splitline = line.split(", ")
        # differentiate test results vs training results files
        if (line == "SUMMARY"):
            is_test_dat = True
        if (is_test_dat and line == "TESTING RESULTS"):
            found_test_dat = True
        if (not is_test_dat or (is_test_dat and found_test_dat)):
            # don't crash if we hit extra new line at end
            if (line == ""):
                continue
            elif (line[0].isdigit()):
                place = []
                place.append(str(splitline[0]))
                place.append(str(str(splitline[1])))
                if (len(line) > 2):
                    orgs = splitline[2:]
                    for id in orgs:
                        word = str("")
                        for letter in id:
                            if (letter != "[" and letter != "'" and letter != "]" and letter != "\"" and letter != " "):
                                word = word + letter
                        orgs = word
                        place.append(orgs)
                sightings.append(place)
    return sightings        

def readSightingsFile(filename):
    lf = open(filename)
    filedata = lf.read()
    lf.close()
    
    if ("\r" in filedata):
        sightings = filedata.split('\r')
    else:
        sightings = filedata.split('\n')
  
    org_locs = []
    i = 0
    for row in sightings:
        if (i != 0):
            this_place = []
            splitline = row.split(",")
            this_place.append(float(splitline[1]))
            this_place.append(float(splitline[2]))
            this_place.append(splitline[0])
            org_locs.append(this_place)
        i += 1
    return org_locs        

def plotResults(outfile, gaHits, plottype, org_sightings):
    camx = []
    camy = []
    seen_orgx = []
    seen_orgy = []
    seen_orgid = []
    orgx = []
    orgy = []
    orgids = []

    for r in org_sightings:
        orgx.append(r[0])
        orgy.append(r[1])
        orgids.append(r[2])

    for s in gaHits:
        camx.append(s[0])
        camy.append(s[1])
        i = 2
        while (i < len(s)):
            seen_orgx.append(s[0])
            seen_orgy.append(s[1])
            seen_orgid.append(s[i])
            i = i + 1

    plot(orgx, orgy, 'D', color = 'black', markersize = 1.2, alpha = 0.7)
    plot(camx, camy, 'x', color = 'red', markersize = 4, alpha = 1)
    plot(seen_orgx, seen_orgy, 'o', color = 'blue', markeredgecolor = 'black', markersize = 6)          

    savefig(outfile)


if __name__ == "__main__":
  main()

