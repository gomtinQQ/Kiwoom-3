# -*- coding: utf-8 -*-

import numpy as np
from numpy import convolve
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
import sys
sys.path.append('../src')
import btsForDaily
import datetime

def movingaverage(values,window):
    
    weights = np.repeat(1.0,window)/window
    sma = np.convolve(values, weights, 'valid')#mode = valid,same,full
    return sma


Data = btsForDaily.daily().getDataFromDaum('021080','2015-10-1') #시,고,저,종,거래량


date_fmt = '%Y-%m-%d'
x=[]
y=[]
dt_x=[]
newAr=[]

fig,ax= plt.subplots()
date_formatter = mdates.DateFormatter('%Y-%m-%d')

ax.xaxis.set_major_formatter(date_formatter)
for time in Data:
    raw_x= datetime.datetime.strptime(str(Data[time][0]),date_fmt)
    
    date = np.float64(mdates.date2num(raw_x))
    open = np.float64(Data[time][1])
    high = np.float64(Data[time][2])
    lowp = np.float64(Data[time][3])
    clop = np.float64(Data[time][4])
    volm = np.float64(Data[time][5])
    
    appendLine =date,open,high,lowp,clop,volm 
    newAr.append(appendLine)
    dt_x.append(raw_x) 
    y.append(int(Data[time][4]))
x=[mdates.date2num(i) for i in dt_x]


yMa_20 = movingaverage(y,20)   #day ma
yMa_10 = movingaverage(y,10)
yMa_60 = movingaverage(y,60)
yMa_120 = movingaverage(y,120)



ax=plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
print(len(newAr))
candlestick_ohlc(ax, newAr, width=.6, colorup='#53c156', colordown='#ff1717')


ax.plot_date(x,y,'r-')

fig.autofmt_xdate()


ax.plot(x[:-(len(x)-len(yMa_10))],yMa_10)
ax.plot(x[:-(len(x)-len(yMa_20))],yMa_20)
ax.plot(x[:-(len(x)-len(yMa_60))],yMa_60,'w-')
ax.plot(x[:-(len(x)-len(yMa_120))],yMa_120)

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

