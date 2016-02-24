# -*- coding: utf-8 -*-
import numpy as np
from numpy import convolve
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import sys
sys.path.append('../src')
import btsForDaily
import datetime

def movingaverage(value,term):
    
    value = pd.Series(value)
    yMa=pd.stats.moments.rolling_mean(value,term)
    return yMa

Data = btsForDaily.daily().getDataFromDaum('021080','2014-9-1')


date_fmt = '%Y-%m-%d'
x=[]
y=[]
dt_x=[]
for time in Data:
    raw_x= datetime.datetime.strptime(str(Data[time][0]),date_fmt)
    dt_x.append(raw_x) 
    y.append(int(Data[time][4]))
    
x=[mdates.date2num(i) for i in dt_x]



yMa_20 = movingaverage(y,20)   #day ma
yMa= movingaverage(y,10)
yMa_60 = movingaverage(y,60)
yMa_120 = movingaverage(y,120)

fig,ax= plt.subplots()

ax.plot_date(x,y,'r-')



date_formatter = mdates.DateFormatter('%Y-%m-%d')

ax.xaxis.set_major_formatter(date_formatter)
fig.autofmt_xdate()
# print(len(x))
# plt.plot(x[:-9],yMa[9:],'b-')
# 
# plt.plot(x[:-9],yMa[9:],'b-')
# print(len(x),len(yMa_10))
# ax.plot(x[:-(len(x)-len(yMa_10))],yMa_10[:(len(x)-len(yMa_10))],'b-')
print(len(x),len(yMa_20))
print(len(x)-len(yMa_20))

ax.plot(x[:346],yMa_20[19:])
# ax.plot(x[:-(len(x)-len(yMa_60))],yMa_60[:-(len(x)-len(yMa_60))])
# ax.plot(x[:-(len(x)-len(yMa_120))],yMa_120[:-(len(x)-len(yMa_120))])

plt.show()


