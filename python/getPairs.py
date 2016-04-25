from __future__ import print_function
import re
import math
import sys

### usage
### python getpairs.py config_filename cutOffPeriodic
### prints the pairs and triplets of configuration 

def validDistance(list1, list2, cutoff):
    distance = math.sqrt((list1[0]-list2[0])**2 + (list1[1]-list2[1])**2 + (list1[2]-list2[2])**2)
    return (distance < cutoff)

def validDistanceWithImageParticles(list1,list2, cutoff, box):
    if (validDistance(list1, list2, cutoff)):
        return True
    else:
        temp = []
        for i in range(0,3):
            dist = list1[i] - list2[i]
            factor = math.floor(dist/box[i]+0.5)
            temp.append(list2[i] + box[i]*factor)
    
        return validDistance(list1, temp, cutoff)
  


box = [19.6288955551,19.6288955551,19.6288955551] #w256
#box = [23.5614871713, 23.5614871713, 27.1863313515] #w512
cutOffPeriodic = (str(sys.argv[2]) == "True")
pairCutoff = 6.5
tripCutoff = 4.5

filename = str(sys.argv[1])
#f = open('./water512/CONFIG.01', 'r')
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

#find all pairs and trip
closePairs = []
closeTriplets = []
for i in range(0, len(oxygenXYZ)):
    for j in range(i+1, len(oxygenXYZ)):
        if (not cutOffPeriodic):
            #if valid pair
            if (validDistance(oxygenXYZ[i], oxygenXYZ[j], pairCutoff)):
                closePairs.append([oxygenXYZ[i][3],oxygenXYZ[j][3]])
                #check for trips
            if (validDistance(oxygenXYZ[i], oxygenXYZ[j], tripCutoff)):
                for k in range(j+1, len(oxygenXYZ)):
                    if (validDistance(oxygenXYZ[i], oxygenXYZ[k], tripCutoff) and (validDistance(oxygenXYZ[j], oxygenXYZ[k], tripCutoff))):
                        closeTriplets.append([oxygenXYZ[i][3], oxygenXYZ[j][3], oxygenXYZ[k][3]])
        else:
            #if valid pair with imaging
            if (validDistanceWithImageParticles(oxygenXYZ[i], oxygenXYZ[j], pairCutoff, box)):
                closePairs.append([oxygenXYZ[i][3],oxygenXYZ[j][3]])
                #check for trips
            if (validDistanceWithImageParticles(oxygenXYZ[i], oxygenXYZ[j], tripCutoff, box)):
                for k in range(j+1, len(oxygenXYZ)):
                    if (validDistanceWithImageParticles(oxygenXYZ[i], oxygenXYZ[k], tripCutoff, box) and (validDistanceWithImageParticles(oxygenXYZ[j], oxygenXYZ[k], tripCutoff, box))):
                        closeTriplets.append([oxygenXYZ[i][3], oxygenXYZ[j][3], oxygenXYZ[k][3]])

print("cutoff periodic:", cutOffPeriodic)
print("number of pairs:",len(closePairs))
print("number of triplets:",len(closeTriplets))

#for pair in closePairs:
#    print(pair)
#for trip in closeTriplets:
#    print(trip)
