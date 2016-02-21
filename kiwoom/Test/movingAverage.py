# -*- coding: utf-8 -*-

import numpy as np
from numpy import convolve
import matplotlib.pyplot as plt


def movingaverage(values,window):
    
    weights = np.repeat(1.0,window)/window
    sma = np.convolve(values, weights, 'valid')
    print(values,weights)
    return sma

x = [1,2,3,4,5,6,7,8,9,10]#x축
y = [3,5,2,4,9,1,7,5,9,1] #y축

yMa = movingaverage(y, 3)   #day ma
# print(yMa)

print(yMa)
plt.plot(x,y)
plt.plot(x[len(x)-len(yMa):],yMa)
# plt.show()


import pandas.io.data as web
import datetime

start = datetime.datetime(2016,1,1)

stock  = web.DataReader("126700.KQ","ff",start)

print(stock)

