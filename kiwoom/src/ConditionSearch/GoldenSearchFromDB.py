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
# import MakeDB
import configparser
import logging

class GoldenSearchFromDB1():
    
    
    
    def keepBuying(self,code,dd,DAY="",FOREIGNER=True,COMPANY=True):
        '''DAY일동안 순매수하면 true, 기관,외국인 모두 알아볼려면 둘다 TRUE'''
        today = datetime.datetime.today()
        
        start = datetime.timedelta(DAY)
        
        length = datetime.datetime.date(today-start)
        
#         dd =YGGetWebData.getForeignerAndCompanyPureBuy(code,length)
        
        day =5
        if DAY!="":
            day=int(DAY)
        dd= dd[-20:]    #20일까지만 본다.
        dd=dd.iloc[::-1]
        FB=True
        CB=True
        for index in range(day):
#             print(index,len(dd))
#             print(dd)
#             print(index,dd['Foreign'][index])
#             print(dd['Foreign'][index],index)
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
    
    def Golden(self,Data):
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
            traceback.print_exc(file=sys.stdout)
            return None
        except Exception as a:
            traceback.print_exc(file=sys.stdout)
            
    def VolumeCheck(self,Data,standard,condition):
        '''가장 최근일을 기준으로 몇일동안 거래량증가했는지 day로 나타냄'''
        '''ex)최근standard 일동안의 거래량이 condition거래량보다 높은지 확인.'''
        '''높으면 거래량 급증이라 판단, return true 그렇지안으면 false'''
        
        
        st=0
        cd=0
        for i in range(standard):
#             print(Data,i)
            st+=int(Data['Volume'][i])
        for i in range(standard ,condition):
    #         print(i)
            cd+=int(Data['Volume'][i])
        
#         print(st,cd)
        flag = False
        if st>cd :
            flag = True
        return flag
        
        
    def Search(self,Code,date,end,YG,bld,timeOut=""):
    #     Data = YGGetWebData.getStockPriceData(Code,date,timeOut)
#         print(Code)
        dd = str(Code)
#         print(dd)
        Data = YG.getClosePriceFromDB(dd)
        if len(Data) <20: #거래일이 20일미만인건 걍 보내주자.
            return
        
    #     print(Data['close'])
        Data['ma5']=DrawGraph2.movingAverage(Data['Close'],5)
        Data['ma20']=DrawGraph2.movingAverage(Data['Close'],20)
        Data['ma60']=DrawGraph2.movingAverage(Data['Close'],60)
        
        Data['Golden_20_5']=Data['ma5']-Data['ma20']
        
        
    #     print(Data['Date'])
        Gold = self.Golden(Data)
        
        try:
            dd =Gold.to_datetime()
            
            date_fmt='%Y-%m-%d'
            end =datetime.datetime.strptime(end,date_fmt)
            
#             if end<dd and self.VolumeCheck(Data,3,7) and self.keepBuying(code,Data,3):
#             if end<dd and self.VolumeCheck(Data,3,7):
            if end<dd and self.keepBuying(code,Data,3):
    #         if end<dd  :
                print('GoldenCross~ Code',Code,' When: ',dd ,end="")
                
                bld.insertGold(str(Code))
                
    
        except Exception as a :
            traceback.print_exc(file=sys.stdout)



if __name__ == '__main__':
    
    
    YG = YGGetCloseDB.YGGetCloseDB()
    YG.setProperties()
    codeNameCoast = YG.getCodeNameCoast()
    
    md = GoldenSearchFromDB1()
    logger = logging.getLogger("YGLogger")
    bld = BuyListDb.BuyListDB()
    bld.setProperties()
#     bld.createDatabase('../../Sqlite3/BuyList'+str(datetime.datetime.today().date())+'.db','BuyList')

    i=0
    for code in range(len(codeNameCoast['Code'])):
        code = codeNameCoast['Code'][code]
        
        md.Search(code,'2016-1-13','2016-02-25',YG,bld)
        i+=1
#         print('Code[',code,'] (',i,'/',len(codeNameCoast),')')
        logger.debug('Code[ %s'%code+'] ( %s'%(i,)+'/ %s'%(len(codeNameCoast))+')')
#         print(' ',i,len(codeNameCoast))