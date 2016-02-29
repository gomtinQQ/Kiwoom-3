# -*- coding: utf-8 -*-
import datetime
import sys
sys.path.append('../')
sys.path.append('../Graph')
sys.path.append('../Data')
import btsForDashin
import YGGetWebData
import DrawGraph2

def keepBuying(code,day=""):
    dd =YGGetWebData.getForeignerAndCompanyPureBuy(code,day)
    return dd

def Golden(Data):
    prev_key,prev_val=0,0
    
    try:
        for key,val in Data['Golden_20_5'].iteritems():
            if val == 0:
                continue
            if val*prev_val < 0 and val > prev_val:
                Gold=Data['Date'][key]
            prev_key,prev_val=key,val
        return Gold 
            
    except UnboundLocalError :
        return None
    except Exception as a:
        pass
        
    
def Search(Code,date,end,timeOut=""):
    Data = YGGetWebData.getStockPriceData(Code,date,timeOut)
    Data['ma5']=DrawGraph2.movingAverage(Data['close'],5)
    Data['ma20']=DrawGraph2.movingAverage(Data['close'],20)
    Data['ma60']=DrawGraph2.movingAverage(Data['close'],60)
    
    Data['Golden_20_5']=Data['ma5']-Data['ma20']
    
    Gold = Golden(Data)
        
    try:
        dd =Gold.to_datetime()
        
        date_fmt='%Y-%m-%d'
        end =datetime.datetime.strptime(end,date_fmt)
        
        if end<dd:
            print('GoldenCross~ Code',Code,' When: ',dd ,end="")
    except Exception as a :
        pass



if __name__ == '__main__':
    
#     keepBuying(126700)
    bfd = btsForDashin.btsForReal()
    codeNameCoast = bfd.UrlParsing()
    i=0
    for code in codeNameCoast:
        for name in codeNameCoast[code]:
            Search(str(code),'2016-1-13','2016-02-25')
            i+=1
            print(' ',i,len(codeNameCoast))