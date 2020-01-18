#!/usr/bin/env python
# module for writing to text file

# get filepath using rospack to get path to package, and then adding on some more stuff
import rospkg
filename = rospkg.RosPack().get_path('lab4') + '/scripts/trajectory.txt'

likely_x = []
likely_y = []
likely_t = []
beliefs = []

def addPoint(x, y, t, b):
    likely_x.append(x)
    likely_y.append(y)
    likely_t.append(t)
    beliefs.append(b)

def writeToFile():
    f = open(filename, 'w') 
    for i in range(len(likely_x)):
        value = (likely_x[i], likely_y[i], likely_t[i])
        f.write(str(value) + '\n')
    
    

