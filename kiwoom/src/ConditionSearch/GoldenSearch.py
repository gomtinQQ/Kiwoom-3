# -*- coding: utf-8 -*-
import datetime
import sys
sys.path.append('../')
sys.path.append('../Graph')
sys.path.append('../Data')
import btsForDashin
import YGGetWebData
import DrawGraph2

def keepBuying(code,DAY="",FOREIGNER=True,COMPANY=True):
    '''DAY일동안 순매수하면 true, 기관,외국인 모두 알아볼려면 둘다 TRUE'''
    dd =YGGetWebData.getForeignerAndCompanyPureBuy(code,DAY)
    day =5
    if DAY!="":
        day=int(DAY)
    
    FB=True
    CB=True
    for index in range(day):
        Foreign = int(dd['Foreign'][index])
        Company = int(dd['Company'][index])
        
        if Foreign <=0:
            FB=False
        if Company <=0:
            CB=False
            
    if FOREIGNER and COMPANY:
        if FB and CB :
            return True
        else:
            return False
        
    if FOREIGNER :
        return FB
    elif COMPANY : 
        return CB 

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
        
def VolumeCheck(Data,standard,condition):
    '''가장 최근일을 기준으로 몇일동안 거래량증가했는지 day로 나타냄'''
    '''ex)최근standard 일동안의 거래량이 condition거래량보다 높은지 확인.'''
    '''높으면 거래량 급증이라 판단, return true 그렇지안으면 false'''
    
    
    st=0
    cd=0
    for i in range(standard):
#         print(i)
        st+=int(Data['volume'][i])
    for i in range(standard ,condition):
#         print(i)
        cd+=int(Data['volume'][i])
        
    flag = False
    if st>cd :
        flag = True
    return flag
    
    
def Search(Code,date,end,timeOut=""):
    Data = YGGetWebData.getStockPriceData(Code,date,timeOut)
    if len(Data) <20: #거래일이 20일미만인건 걍 보내주자.
        return
    
    Data['ma5']=DrawGraph2.movingAverage(Data['close'],5)
    Data['ma20']=DrawGraph2.movingAverage(Data['close'],20)
    Data['ma60']=DrawGraph2.movingAverage(Data['close'],60)
    
    Data['Golden_20_5']=Data['ma5']-Data['ma20']
    
    Gold = Golden(Data)
    
    try:
        dd =Gold.to_datetime()
        
        date_fmt='%Y-%m-%d'
        end =datetime.datetime.strptime(end,date_fmt)
        
        if end<dd and VolumeCheck(Data, 3, 7) and keepBuying(code,2) :
            print('GoldenCross~ Code',Code,' When: ',dd ,end="")
    except Exception as a :
        print(Exception,a)
        pass



if __name__ == '__main__':
    
#     print(keepBuying(126700,30))
#     Search(115180,'2016-1-13','2016-02-25')
    bfd = btsForDashin.btsForReal()
    codeNameCoast = bfd.UrlParsing()
    i=0
    for code in codeNameCoast:
        for name in codeNameCoast[code]:
            Search(str(code),'2016-1-13','2016-02-25')
#             if keepBuying(code):
#                 print(code)
            i+=1
            print(' ',i,len(codeNameCoast))