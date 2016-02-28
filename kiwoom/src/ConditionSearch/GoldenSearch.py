# -*- coding: utf-8 -*-
import datetime
import sys
sys.path.append('../')
sys.path.append('../Graph')
import DrawGraph2
import btsForDashin



def Search(Code,date,end,timeOut=""):
    Data = DrawGraph2.getData(Code,date,timeOut)
    Data['ma5']=DrawGraph2.movingAverage(Data['close'],5)
    Data['ma20']=DrawGraph2.movingAverage(Data['close'],20)
    Data['ma60']=DrawGraph2.movingAverage(Data['close'],60)
    
    Data['Golden_20_5']=Data['ma5']-Data['ma20']
    
    prev_key,prev_val=0,0
#     Gold=[]
#     Dead=[]
    for key,val in Data['Golden_20_5'].iteritems():
        if val == 0:
            continue
        if val*prev_val < 0 and val > prev_val:
            
#             Gold.append(Data['Date'][key])
            Gold=Data['Date'][key]
        if val*prev_val < 0 and val < prev_val:
            Dead=Data['Date'][key]
#             Dead.append(Data['Date'][key])
        prev_key,prev_val=key,val
    try:
        dd =Gold.to_datetime()
    
        
    #     day = str(dd.year)+str(dd.month)+str(dd.day)
        
        date_fmt='%Y-%m-%d'
        end =datetime.datetime.strptime(end,date_fmt)
        
        if end<dd:
            
            print('GoldenCross~ Code',Code,' When: ',dd ,end="")
#         else:
#             print('Not happened!')
    
    except Exception as a :
#         print(a)
        pass
        
bfd = btsForDashin.btsForReal()
codeNameCoast = bfd.UrlParsing()
i=0
for code in codeNameCoast:
    for name in codeNameCoast[code]:
        Search(str(code),'2016-1-13','2016-02-15')
        i+=1
        print(' ',i,len(codeNameCoast))