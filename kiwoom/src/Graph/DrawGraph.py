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
    
    
#     date_formatter = mdates.DateFormatter(date_fmt)
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
    
    dd = pd.DataFrame(pdAr,columns=['Date','open','high','low','close','volume'])
    dd.reset_index(inplace = True)
    dd.Date=mdates.date2num(dd.Date.dt.to_pydatetime())
    
    yMa_5 = movingAverage(dd['close'], 5)
    yMa_20 = movingAverage(dd['close'],20)   #day ma
    golden_20_5    =   yMa_20-yMa_5
    
    fig,ax = plt.subplots()
#     ax.xaxis.set_major_locator(mticker.MaxNLocator(10))    #set x locator interva

    SP = len(dd.Date[19:])
    ax.plot_date(dd['Date'][-SP:],dd['close'][-SP:],'-')

    uu = [tuple(x) for x in dd[['Date', 'open', 'high', 'low', 'close']].to_records(index=False)]
     
    candlestick_ohlc(ax, uu[-SP:], width=.6, colorup='red', colordown='blue')
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_fmt)) # 날짜포맷으로 바꿔줌.
    fig.autofmt_xdate() #날짜포맷  이쁘게정렬됨.
    
    
    Label1='5 SMA'
    Label2='20 SMA'
    
    ax.plot(dd['Date'][-SP:],yMa_5[-SP:],label=Label1,linewidth=1.)
    ax.plot(dd['Date'][-SP:],yMa_20[-SP:],label=Label2,linewidth=1.)

    plt.legend(loc='best')
    
    
    prev_key=prev_val=0
    
    for key,val in golden_20_5.iteritems():
        if val ==0:
            continue
        if val*prev_val < 0 and val > prev_val:
            ax.annotate('GOLDEN',xy=(dd['Date'][-SP:][key],yMa_20[key]),xytext=(10,-30),textcoords='offset points',arrowprops=dict(facecolor='red',arrowstyle="->"))
        if val*prev_val < 0 and val < prev_val:
            ax.annotate('DEAD',xy=(dd['Date'][-SP:][key],yMa_20[key]),xytext=(10,30),textcoords='offset points',arrowprops=dict(facecolor='blue', arrowstyle="->"))
        prev_key,prev_val=key,val
    
    axv = ax.twinx()
    volumeMin=0
    axv.fill_between(dd['Date'][-SP:],volumeMin,volume[-SP:], facecolor='#00ffe8', alpha=.4)
    axv.axes.yaxis.set_ticklabels([]) #set text value
    
    ###Edit this to 3, so it's a bit larger
    axv.set_ylim(0, 3*volume.max())
    axv.tick_params(axis='x', colors='w')
    axv.tick_params(axis='y', colors='w')
    
    plt.show()
    
    
drawGraph('021080','2014-9-1')