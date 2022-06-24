#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 18:24:27 2022

@author: Rasmus Erlemann
"""

import numpy
import matplotlib.pyplot as plt

#Draw 10 simulations from N(0,1)
mu, sigma, n = 0, 1, 5
x = numpy.random.normal(mu, sigma, n)

#Put a ball around the simulations
a,b = min(x), max(x)

#Put a grid on the parameter space R2
G = []
for ind1 in [x / 100 for x in range(-200, 200, 1)]:
    for ind2 in [x / 100 for x in range(1, 200, 1)]:
        G.append([ind1, ind2])

#Sample from the normal distribution with the grid point as parameters 100 times and check if 100*(1-alpha)
#land in the ball around the simulations
cmu = []
csigma = []
sim = 1000
for param in G:
    y = numpy.random.normal(param[0], param[1], sim)
    y = numpy.sort(y)
    check1 = y[int(len(y)*0.025)] > a
    check2 = y[int(len(y)*0.975)] < b
    if check1 and check2:
        cmu.append(param[0])
        csigma.append(param[1])
        
#Visualize the confidence set 
plt.plot(cmu, csigma, '*')
plt.xlabel("Mean")
plt.ylabel("Variance")
plt.show()

#Visualize the confidence distribution for the mean
#plt.hist(cmu, bins=50)
#plt.show()

