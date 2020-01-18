#!/usr/bin/env python
# module for handling numerical data

import math

LINEAR_LENGTH = 7
LINEAR_UNIT = 0.2

EULER_LENGTH = 360
EULER_UNIT = 45

def LU():
    return LINEAR_UNIT

def LL():
    return LINEAR_LENGTH

def EU():
    return EULER_UNIT

def EL():
    return EULER_LENGTH

# functions for discrete/continous conversions
def getDiscreteMetres(metre):
    return int(math.ceil(metre/LINEAR_UNIT))

def getDiscreteEulerAngle(angle):
    return int(math.ceil(angle/EULER_UNIT))

def getContinousMetres(metre):
    return (metre*LINEAR_UNIT - LINEAR_UNIT/2)

def getContinousEulerAngle(angle):
    return (angle*EULER_UNIT - EULER_UNIT/2)

# for this length and this discretization size, how many total discrete data points will I have?
def getNumDatapoints():
    d = LINEAR_LENGTH/LINEAR_UNIT
    t = EULER_LENGTH/EULER_UNIT
    return int(d), int(t)

# used to get distance between two points
def deltaTranslation(sx, sy, tx, ty):
    sx = getContinousMetres(sx)
    sy = getContinousMetres(sy)
    tx = getContinousMetres(tx)
    ty = getContinousMetres(ty)
    return math.sqrt(math.pow((sx - tx), 2) + math.pow((sy - ty), 2))

# used when you have a point and a direction, and need to rotate towards another point
	# the prefix s is source, the prefix t is target
def deltaRotation1(sx, sy, stheta, tx, ty):
    sx = getContinousMetres(sx)
    sy = getContinousMetres(sy)
    stheta = getContinousEulerAngle(stheta)
    tx = getContinousMetres(tx)
    ty = getContinousMetres(ty)
    ttheta = math.atan2(ty - sy, tx - sx) * 180/3.14
    # map [-pi, pi] to [0, 2pi]
    if ttheta < 0:
        ttheta = 360 + ttheta
    diff = ttheta - stheta
    # map [0,2pi] to [-pi, pi]
    if diff > 180:
        diff = diff - 360
    return diff, ttheta

# used when you have a rotation, and need to rotate towards some other absolute angle
def deltaRotation2(stheta, ttheta):
    ttheta = getContinousEulerAngle(ttheta)
    diff = ttheta - stheta
    # map [0,2pi] to [-pi, pi]
    if diff > 180:
        diff = diff - 360
    return diff

