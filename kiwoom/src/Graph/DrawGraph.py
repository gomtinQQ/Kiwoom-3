# -*- coding: utf-8 -*-
import numpy as np
from numpy import convolve
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
import matplotlib.finance as fn
import sys
from matplotlib.dates import date2num
sys.path.append('../')
import btsForDaily
import datetime
import time
import pandas as pd

def movingAverage(values,window):
    
    value = pd.Series(values)
    yMa=pd.stats.moments.rolling_mean(value,window)
    return yMa

def getData(code,date):
    return btsForDaily.daily().getDataFromDaum(str(code),str(date))

def drawGraph(code,date):
    Data = getData(code,date)
    date_fmt = '%Y-%m-%d'
    
    x=[]
    y=[]
    dt_x=[]
    newAr=[]
    pdAr=[]
    volumeArr=[]
    
    fig,ax = plt.subplots()
    date_formatter = mdates.DateFormatter(date_fmt)
    ax.xaxis.set_major_formatter(date_formatter)
    for price in Data:
        raw_x = datetime.datetime.strptime(str(Data[price][0]),date_fmt)
        
        date = np.float64(mdates.date2num(raw_x))
        open = np.float64(Data[price][1])
        high = np.float64(Data[price][2])
        lowp = np.float64(Data[price][3])
        clop = np.float64(Data[price][4])
        volume = np.float64(Data[price][5])
        volumeArr.append(volume)
        
        appendLine =date,open,high,lowp,clop 
        newAr.append(appendLine)
        appendPDLine =raw_x,open,high,lowp,clop,volume
        pdAr.append(appendPDLine)
        dt_x.append(raw_x) 
        y.append(clop)
        
    
    volume=np.array(volumeArr)  #ndarray로 변형.
    
    dd = pd.DataFrame(pdAr,columns=['Date','open','high','low','cloe','volume'])
    
    x=[mdates.date2num(i) for i in dt_x]
    yMa_5 = movingAverage(y, 5)
    yMa_20 = movingAverage(y,20)   #day ma
    yMa_10 = movingAverage(y,10)
    yMa_60 = movingAverage(y,60)
    yMa_120 = movingAverage(y,120)
    golden_20_5    =   yMa_5-yMa_20
    
    
    ax.xaxis.set_major_locator(mticker.MaxNLocator(10))    #set x locator interva
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_fmt))
    candlestick_ohlc(ax, newAr, width=.6, colorup='red', colordown='blue')

    ax.plot_date(x,y,'r-')
    
    
    fig.autofmt_xdate()
    
    Label1='5 SMA'
    Label2='20 SMA'
    
    label = ax.plot(x[:-4],yMa_5[4:],label=Label1,linewidth=1.5)
    label2 =ax.plot(x[:-9],yMa_10[9:],label=Label2,linewidth=1.5)
    
    plt.legend(loc=9,ncol=2,prop={'size':7},fancybox=True)
    
    ax.plot(x[:-19],yMa_20[19:])
    ax.plot(x[:-59],yMa_60[59:])
    ax.plot(x[:-119],yMa_120[119:])
    
    prev_key=prev_val=0
    
    for key,val in golden_20_5[1:].iteritems():
        if val ==0:
            continue
        if val*prev_val < 0 and val > prev_val:
            ax.annotate('GOLDEN',xy=(x[key],yMa_20[key]),xytext=(10,-30),textcoords='offset points',arrowprops=dict(facecolor='black', shrink=0.05))
        if val*prev_val < 0 and val < prev_val:
            ax.annotate('DEAD',xy=(x[key],yMa_20[key]),xytext=(10,30),textcoords='offset points',arrowprops=dict(facecolor='black', shrink=0.05))
        prev_key,prev_val=key,val
    
    axv = ax.twinx()
    volumeMin=0
    axv.fill_between(x,volumeMin,volume, facecolor='#00ffe8', alpha=.4)
    axv.axes.yaxis.set_ticklabels([]) #set text value
    
    ###Edit this to 3, so it's a bit larger
    axv.set_ylim(0, 3*volume.max())
    axv.tick_params(axis='x', colors='w')
    axv.tick_params(axis='y', colors='w')
    
    plt.show()
    
    
drawGraph('021080','2014-9-1')