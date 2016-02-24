# -*- coding: utf-8 -*-

import numpy as np
from numpy import convolve
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
sys.path.append('../src')
import btsForDaily
import datetime

def movingaverage(values,window):
    
    weights = np.repeat(1.0,window)/window
    sma = np.convolve(values, weights, 'valid')#mode = valid,same,full
    # sma = np.correlate(values, weights, 'full')
#     print(values,weights)
    return sma


Data = btsForDaily.daily().getDataFromDaum('126700','2014-9-1')


date_fmt = '%Y-%m-%d'
x=[]
y=[]
dt_x=[]
for time in Data:
    raw_x= datetime.datetime.strptime(str(Data[time][0]),date_fmt)
    dt_x.append(raw_x) 
    y.append(int(Data[time][1]))
x=[mdates.date2num(i) for i in dt_x]


yMa_20 = movingaverage(y,20)   #day ma
yMa_10 = movingaverage(y,10)
yMa_60 = movingaverage(y,60)


fig,ax= plt.subplots()

ax.plot_date(x,y,'r-')
date_formatter = mdates.DateFormatter('%Y-%m-%d')

ax.xaxis.set_major_formatter(date_formatter)
fig.autofmt_xdate()

# print(len(x),len(yMa))
ax.plot(x[:-(len(x)-len(yMa_10))],yMa_10,'b-')
ax.plot(x[:-(len(x)-len(yMa_20))],yMa_20)
ax.plot(x[:-(len(x)-len(yMa_60))],yMa_60)

plt.show()

# 
# import pandas.io.data as web
# import datetime
# 
# start = datetime.datetime(2016,1,1)
# 
# stock  = web.DataReader("126700.KQ","ff",start)
#
# print(stock)

