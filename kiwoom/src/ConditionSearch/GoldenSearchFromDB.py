# -*- coding: utf-8 -*-
import datetime
import sys,traceback
sys.path.append('../')
sys.path.append('../Graph')
sys.path.append('../Data')
sys.path.append('../DB')
import btsForDashin
import YGGetWebData
import YGGetCloseDB
import DrawGraph2
import BuyListDb
import MakeDB


def keepBuying(code,DAY="",FOREIGNER=True,COMPANY=True):
    '''DAY일동안 순매수하면 true, 기관,외국인 모두 알아볼려면 둘다 TRUE'''
    today = datetime.datetime.today()
    
    start = datetime.timedelta(DAY)
    
    length = datetime.datetime.date(today-start)
    
    dd =YGGetWebData.getForeignerAndCompanyPureBuy(code,length)
    
    day =5
    if DAY!="":
        day=int(DAY)
    
    FB=True
    CB=True
    for index in range(len(dd)):
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
        Gold =None
#         print(Data['Golden_20_5'])
        for key,val in Data['Golden_20_5'].iteritems():
#             print(key,val)
            if val == 0:
                continue
            if val*prev_val < 0 and val > prev_val:
                Gold=Data['Date'][key]
#                 print(Gold)
#                 print(val,prev_val)
            prev_key,prev_val=key,val
        return Gold 
            
    except UnboundLocalError :
        print(MakeDB.DBMake().PrintException())
        return None
    except Exception as a:
        print(MakeDB.DBMake().PrintException())
        
def VolumeCheck(Data,standard,condition):
    '''가장 최근일을 기준으로 몇일동안 거래량증가했는지 day로 나타냄'''
    '''ex)최근standard 일동안의 거래량이 condition거래량보다 높은지 확인.'''
    '''높으면 거래량 급증이라 판단, return true 그렇지안으면 false'''
    
    
    st=0
    cd=0
    for i in range(standard):
#         print(Data)
        st+=int(Data['Volume'][i])
    for i in range(standard ,condition):
#         print(i)
        cd+=int(Data['Volume'][i])
        
    flag = False
    if st>cd :
        flag = True
    return flag
    
    
def Search(Code,date,end,YG,timeOut=""):
#     Data = YGGetWebData.getStockPriceData(Code,date,timeOut)
    Data = YG.getClosePriceFromDB(str(Code))
    if len(Data) <20: #거래일이 20일미만인건 걍 보내주자.
        return
    
#     print(Data['close'])
    Data['ma5']=DrawGraph2.movingAverage(Data['Close'],5)
    Data['ma20']=DrawGraph2.movingAverage(Data['Close'],20)
    Data['ma60']=DrawGraph2.movingAverage(Data['Close'],60)
    
    Data['Golden_20_5']=Data['ma5']-Data['ma20']
    
    
#     print(Data['Date'])
    Gold = Golden(Data)
    
    try:
        dd =Gold.to_datetime()
        
        date_fmt='%Y-%m-%d'
        end =datetime.datetime.strptime(end,date_fmt)
        
        if end<dd and VolumeCheck(Data,3,7) and keepBuying(code,2):
#         if end<dd  :
            print('GoldenCross~ Code',Code,' When: ',dd ,end="")
            bld = BuyListDb.BuyListDB()
            bld.setProperties()
            bld.insertGold(str(Code))
            

    except Exception as a :
        traceback.print_exc(file=sys.stdout)



if __name__ == '__main__':
    
    YG = YGGetCloseDB.YGGetCloseDB()
    YG.setProperties()
    codeNameCoast = YG.getCodeNameCoast()
    i=0
#     Search('126700', '2016-01-13', '2016-02-25', YG,)
    for code in range(len(codeNameCoast['Code'])):
        code = codeNameCoast['Code'][code]
        
        Search(code,'2016-1-13','2016-02-25',YG)
        i+=1
        print('Code[',code,'] (',i,'/',len(codeNameCoast),')')
#         print(' ',i,len(codeNameCoast))