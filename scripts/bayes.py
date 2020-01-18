#!/usr/bin/env python
# module for dealing with the bayesian belief model
from __future__ import print_function
from __future__ import division

import data
import math
import numpy as np

d, t = data.getNumDatapoints()

beliefs = [[[0.0 for i in range(t)] for j in range(d)] for k in range(d)]

rot_dev = data.EU() + data.EU()/2
lin_dev = data.LU() + data.LU()/2

def getBeliefs():
    return beliefs

def getMostLikely():
    mx = 0
    my = 0
    mt = 0
    for i in range(d):
        for j in range(d):
            for k in range(t):
                if beliefs[i][j][k] > beliefs[mx][my][mt]:
                    mx = i
                    my = j
                    mt = k
    return mx, my, mt

def getBelief(i, j, k):
    return beliefs[i][j][k]

def gaussian(x, mu, sigma):
    u = (x-mu)/abs(sigma)
    y = (1/(math.sqrt(2*math.pi)*abs(sigma)))*math.exp(-u*u/2)
    return y

def setInitialBeliefs(x, y, theta):
    total = 0
    x = data.getContinousMetres(x)
    y = data.getContinousMetres(y)
    theta = data.getContinousEulerAngle(theta)
    for i in range(d):
        for j in range(d):
            for k in range(t):
                p1 = gaussian(data.getContinousMetres(i), x, lin_dev)
                p2 = gaussian(data.getContinousMetres(j), y, lin_dev)
                p3 = gaussian(data.getContinousEulerAngle(k), theta, rot_dev)
                beliefs[i][j][k] = p1*p2*p3
                total = total + beliefs[i][j][k]
                # print(p1, p2, p3, beliefs[i][j][k], total)
    run_normalization(total)

def filter(a1, tr, a2, l, r, b):
    run_prediction(a1, tr, a2)
    print("Prediction complete")
    eta = run_updation(l, r, b)
    print("Updation complete")
    run_normalization(eta)
    print("Normalized")
    pass

def run_prediction(a1, tr, a2):
    for i1 in range(d):
        for j1 in range(d):
            for k1 in range(t):
                sigma = 0
                for i2 in range(d):
                    for j2 in range(d):
                        for k2 in range(t):
                            new_a1, ttheta = data.deltaRotation1(i2, j2, k2, i1, j1)
                            new_tr = data.deltaTranslation(i2, j2, i1, j1)
                            new_a2 = data.deltaRotation2(ttheta, k1)
                            p1 = gaussian(new_a1, a1, rot_dev)
                            p2 = gaussian(new_tr, tr, lin_dev)
                            p3 = gaussian(new_a2, a2, rot_dev)
                            sigma = sigma + p1*p2*p3*beliefs[i2][j2][k2]
                beliefs[i1][j1][k1] = sigma
                print("One cell predicted:", i1, j1, k1, beliefs[i1][j1][k1])

landmark_x = [1.25, 1.25, 1.25, 4.25, 4.25, 4.25]
landmark_y = [5.25, 3.25, 1.25, 1.25, 3.25, 5.25]
def run_updation(l, r, b):
    ref_x = data.getDiscreteMetres(landmark_x[l])
    ref_y = data.getDiscreteMetres(landmark_y[l])
    total = 0
    for i in range(d):
        for j in range(d):
            for k in range(t):
                new_r = data.deltaTranslation(i, j, ref_x, ref_y)
                new_b, ttheta = data.deltaRotation1(i, j, k, ref_x, ref_y)
                p1 = gaussian(new_r, r, lin_dev)
                p2 = gaussian(new_b, b, rot_dev)
                beliefs[i][j][k] = p1*p2*beliefs[i][j][k]
                total = total + beliefs[i][j][k]
    return total

def run_normalization(total):
    for i in range(d):
        for j in range(d):
            for k in range(t):
                beliefs[i][j][k] = beliefs[i][j][k]/total

