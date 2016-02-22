# -*- coding: utf8 -*- 
import numpy as np
import pandas as pd
import sqlite3
import datetime
import matplotlib
import matplotlib.pyplot as plt
import pickle
from scipy import stats

conn = sqlite3.connect('stocks.db')
c = conn.cursor()

def get_df(ccode):
    df = pd.read_sql('SELECT * FROM stocks{0} ORDER BY date'.format(ccode), conn, index_col='date')
    df.index = [datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in df.index]
    df.index.name = 'date'
    return df

def golden_vs_death(short_term=50, long_term=200):
    ccodes = [i[0] for i in c.execute('SELECT ccode FROM brand_data ORDER BY ccode').fetchall()]
    all = 0
    nice = 0
    for ccode in ccodes:
        df = get_df(ccode)
        if len(df) <= short_term:
            continue
        mavg_short = pd.rolling_mean(df['close'], short_term)
        mavg_long = pd.rolling_mean(df['close'], long_term)
        df['mavg_short'] = pd.Series(mavg_short, index=df.index)
        df['mavg_long'] = pd.Series(mavg_long, index=df.index)
        df['fluctuation'] = df['mavg_short'] - df['mavg_long']
        df = df[long_term:]
        signal = {}
#         signal stocks date and golden cross (BUY) or death cross (SELL)
        for i, j in enumerate(df['fluctuation']):
            cond1_long = df['mavg_long'].iloc[i] - df['mavg_long'].iloc[i - 1] > 0
            cond2_long = df['mavg_long'].iloc[i - 1] - df['mavg_long'].iloc[i - 2] > 0
            cond3 = abs(df.ix[i - 30:i, 'mavg_short'].mean() - df.ix[i - 30:i, 'mavg_long'].mean()) < df .ix = "" cond_t = "stats.ttest_rel(df.ix[i-10:i," df.ix = "" i - 10:i = "" i - 30:i = "" mavg_long = "" mavg_short = "" std = "" > 0.05  # no difference between short and long mavg before GC
            if i == 0:
                continue            
                # also watch long term moving averages go up or down    
            elif df['fluctuation'].iloc[i] > 0 and df['fluctuation'].iloc[i - 1] < 0 data - blogger - escaped - and = "" data - blogger - escaped - cond_t: = "" data - blogger - escaped - df.index = "" data - blogger - escaped - df = "" data - blogger - escaped - elif = "" data - blogger - escaped - fluctuation = "" data - blogger - escaped - i - 1 = "" data - blogger - escaped - i = "" data - blogger - escaped - iloc = "" data - blogger - escaped - signal = "" > 0:
                signal[df.index[i]] = 'SELL'
            else:
                continue
        if len(signal) > 1:
 
            kys = sorted(signal)
            for i, j in enumerate(kys):
                prev_day = kys[i - 1]
                the_day = j
                if i == 0:
                    pass
                elif signal[prev_day] == 'SELL' and signal[the_day] == 'BUY':
                    all += 1
                    if df['close'].loc[prev_day] > df['close'].loc[the_day]:
                        print(ccode, prev_day.date(), df['close'].loc[prev_day], 'SELL', '->', j.date(), df['close'].loc[the_day], 'BUY RIGHT')
                        nice += 1
                    else:
                        print(ccode, prev_day.date(), df['close'].loc[prev_day], 'SELL', '->', j.date(), df['close'].loc[the_day], 'BUY')
                elif signal[prev_day] == 'BUY' and signal[the_day] == 'SELL':
                    all += 1
                    if df['close'].loc[prev_day] < df['close'].loc[the_day]:
                        print(ccode, prev_day.date(), df['close'].loc[prev_day], 'BUY', '->', j.date(), df['close'].loc[the_day], 'SELL RIGHT')
                        nice += 1
                    else:
                        print(ccode, prev_day.date(), df['close'].loc[prev_day], 'BUY', '->', j.date(), df['close'].loc[the_day], 'SELL')
                else:
                    pass
    print('{0}/{1} = {2}%'.format(nice, all, round(100 * nice / all, 1)))
 
golden_vs_death(short_term=5, long_term=25)
<! - -0 - -></df > 
