from __future__ import print_function
import re
import math

### usage
### python getpairs.py 
### prints the pairs and triplets of configuration 

############### parameters ####################################################
#filename = "./equilibrated_boxes/w256.01"
filename = "./equilibrated_boxes/w512.01"

#box = [19.6288955551,19.6288955551,19.6288955551] #w256
box = [23.5614871713, 23.5614871713, 27.1863313515] #w512

pairCutoffMin = 2
pairCutoffMax = 6.5

tripCutoffMin = 2
tripCutoffMax = 4.5

cutOffPeriodic = True


def validDistance(list1, list2, cutoffMax, cutoffMin):
    distance = math.sqrt((list1[0]-list2[0])**2 + (list1[1]-list2[1])**2 + (list1[2]-list2[2])**2)
    #print("{} and {} distance = {}".format(list1[3], list2[3], distance))
    return (cutoffMin < distance) and (distance < cutoffMax) 

def validDistanceWithImageParticles(list1,list2, cutoffMax, cutoffMin, box):
#    if (validDistance(list1, list2, cutoffMax, cutoffMin)):
#        return True
#    else:
    temp = []
    for i in range(0,3):
        dist = list1[i] - list2[i]
        factor = math.floor(dist/box[i]+0.5)
        temp.append(list2[i] + box[i]*factor)
    temp.append(list2[3])

    return validDistance(list1, temp, cutoffMax, cutoffMin)

def validPair(list1, list2):
    return validDistance(list1, list2, pairCutoffMax, pairCutoffMin)

def validPairWithImaging(list1, list2):
    return validDistanceWithImageParticles(list1, list2, pairCutoffMax, pairCutoffMin, box)

def validTrip(listA, listB, listC):
    validAB = validDistance(listA, listB, tripCutoffMax, tripCutoffMin) 
    validAC = validDistance(listA, listC, tripCutoffMax, tripCutoffMin)
    validBC = validDistance(listB, listC, tripCutoffMax, tripCutoffMin)
    return (validAB and validAC) or (validAB and validBC) or (validAC and validBC)
    #return validAB and validAC and validBC

def validTripWithImaging(listA, listB, listC):
    validAB = validDistanceWithImageParticles(listA, listB, tripCutoffMax, tripCutoffMin, box)
    validAC = validDistanceWithImageParticles(listA, listC, tripCutoffMax, tripCutoffMin, box)
    validBC = validDistanceWithImageParticles(listB, listC, tripCutoffMax, tripCutoffMin, box)
    return (validAB and validAC) or (validAB and validBC) or (validAC and validBC)
    #return validAB and validAC and validBC

############### parse oxygen data from file ###################################
def loadOxygen():
    f = open(filename)
    oxygenXYZ = []
    for line in f:
        if "OW" in line:
            location = f.readline()
            xyzn = re.findall("-?\d+.\d+[[eE]?[-+]?\d+]?", location)
            xyzn.append(re.findall('\d+', line)[0])
            oxygenXYZ.append(xyzn)
            for i in range(0, len(xyzn)):
                xyzn[i] = float(xyzn[i])
    f.close()
    return oxygenXYZ


############## Find all pairs and triplets O(n^3) ############################
#find all pairs and trip
def main():
    oxygenXYZ = loadOxygen()
    closePairs = []
    closeTriplets = []
    for i in range(0, len(oxygenXYZ)):
        for j in range(i+1, len(oxygenXYZ)):
            if (not cutOffPeriodic):
                #if valid pair
                if (validPair(oxygenXYZ[i], oxygenXYZ[j])):
                    closePairs.append([oxygenXYZ[i][3],oxygenXYZ[j][3]])
                    #check for trips
                for k in range(j+1, len(oxygenXYZ)):
                    if(validTrip(oxygenXYZ[i], oxygenXYZ[j], oxygenXYZ[k])):
                        closeTriplets.append([oxygenXYZ[i][3], oxygenXYZ[j][3], oxygenXYZ[k][3]])
            else:
                #if valid pair with imaging
                if (validPairWithImaging(oxygenXYZ[i], oxygenXYZ[j])):
                    closePairs.append([oxygenXYZ[i][3],oxygenXYZ[j][3]])
                    #check for trips
                for k in range(j+1, len(oxygenXYZ)):
                    if (validTripWithImaging(oxygenXYZ[i], oxygenXYZ[j], oxygenXYZ[k])):
                        closeTriplets.append([(oxygenXYZ[i][3]-1)/3, (oxygenXYZ[j][3]-1)/3, (oxygenXYZ[k][3]-1)/3])
    
    print("cutoff periodic:", cutOffPeriodic)
    print("number of pairs:",len(closePairs))
    print("number of triplets:",len(closeTriplets))
    
    #for pair in closePairs:
    #    print(pair)
    #for trip in closeTriplets:
    #    print(trip)

main()
#oxygenXYZ = loadOxygen()
