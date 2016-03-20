# -*- coding: utf-8 -*-
import datetime,time
import sys,traceback
sys.path.append('../')
sys.path.append('../Graph')
sys.path.append('../Data')
sys.path.append('../DB')
import btsForDashin
import YGGetCloseDB
import DrawGraph2
import BuyListDb
# import MakeDB
import configparser
import logging
import YGBuyListDB
class GoldenSearchFromDB1():
    
    
    
    def keepBuying(self,code,dd,DAY="",FOREIGNER=True,COMPANY=True):
        '''DAY일동안 순매수하면 true, 기관,외국인 모두 알아볼려면 둘다 TRUE'''
        try:
            today = datetime.datetime.today()
            
            start = datetime.timedelta(DAY)
            
            length = datetime.datetime.date(today-start)
            
            day =5
            if DAY!="":
                day=int(DAY)
            dd= dd[-20:]    #20일까지만 본다.
            dd=dd.iloc[::-1]
            FB=True
            CB=True
#             print(dd)
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
        except :
            YG.debug(traceback.print_exc())
    
    def Golden(self,Data):
        '''기본적으로 5일선이 20일선 돌파하면 골든, 반대면 데드로 판단'''
        
        prev_key=0
        prev_val=0
        
        try:
            Gold =None
            for key,val in Data['Golden_20_5'].iteritems():
                if val == 0:
                    continue
                if val*prev_val < 0 and val > prev_val:
                    Gold=Data['Date'][key]
                prev_key,prev_val=key,val
            return Gold
                
        except UnboundLocalError :
            YG.debug(traceback.print_exc())
        except Exception as a:
            YG.debug(traceback.print_exc())
            
    def VolumeCheck(self,Data,standard,condition):
        '''가장 최근일을 기준으로 몇일동안 거래량증가했는지 day로 나타냄'''
        '''ex)최근standard 일동안의 거래량이 condition거래량보다 높은지 확인.'''
        '''높으면 거래량 급증이라 판단, return true 그렇지안으면 false'''
        
        
        st=0
        cd=0
#         print(Data)
        
        for i in range(standard):
#             print(Data,i)
            st+=int(Data['Volume'][i])
        for i in range(standard ,condition):
#             print(i)
            cd+=int(Data['Volume'][i])
        
#         print(st,cd)
        flag = False
        if st>cd :
            flag = True
        return flag
        
        
    def Search(self,Code,end,YG,bld,DBLog,timeOut=""):
        Data = YG.getClosePriceFromDB(str(Code))
        
        if len(Data) <20: #거래일이 20일미만인건 걍 보내주자.
            return
        
        Data['ma5']=DrawGraph2.movingAverage(Data['Close'],5)
        Data['ma20']=DrawGraph2.movingAverage(Data['Close'],20)
        Data['ma60']=DrawGraph2.movingAverage(Data['Close'],60)
        
        Data['Golden_20_5']=Data['ma5']-Data['ma20']
        
        
        Gold = self.Golden(Data)
        
        try:
            dd =Gold.to_datetime()
            
            date_fmt='%Y-%m-%d'
            end =datetime.datetime.strptime(end,date_fmt)
            
            if end<dd and self.keepBuying(Code,Data,2):
                
                print('keepBuying~ Code',Code,' When: ',dd ,end="")
                self.goldenCount+=1
                self.keepbuy+=1
                YG.debug('keepBuying ~ [%s'%Code+'] DATE [ %s'%dd+']')
                
                if DBLog:
                    bld.insertGold(str(Code))
                
            elif end<dd and self.VolumeCheck(Data,3,20):
                
                print('Volume!~ Code',Code,' When: ',dd ,end="")
                self.goldenCount+=1
                self.volcheck+=1
                YG.debug('Volume!~ [%s'%Code+'] DATE [ %s'%dd+']')
                
                if DBLog:
                    bld.insertGold(str(Code))
                
        except Exception as a :
            print(traceback.print_exc())
#             YG.debug(traceback.print_exc()) 안먹히는 이유를 모르겠음. 

    def createSearchingDB(self,YG):
        
#         YG = YGGetCloseDB.YGGetCloseDB()
#         YG.setProperties()
        start_time = time.time()
        codeNameCoast = YG.getCodeNameCoast()
        
        
#         bld = BuyListDb.BuyListDB()
        BuyListDb.BuyListDB().createDefaultDB()
#         print(bld.BuyListDBToday)    16.3.30
#         bld.createDefaultDB()
        bld = YGBuyListDB.YGGetDbData()
        bld.setProperties(bld.BuyListDBToday,bld.BuyListTable)
        i=0
        self.goldenCount = 0
        self.keepbuy=0
        self.volcheck=0
        DBLog=True
        print("DB LOG [",DBLog,"]")
        for code in range(len(codeNameCoast['Code'])):
            code = codeNameCoast['Code'][code]
            
            self.Search(code,'2016-02-25',YG,bld,DBLog)
            i+=1
            YG.debug('Code[%s'%code+'] ( %s'%(i,)+'/ %s'%(len(codeNameCoast))+')')
        takeTime=time.time()-start_time
        YG.debug('Total Golden Count [%s'%self.goldenCount+'] keepbuying[%s'%self.keepbuy+'] Volume[%s'%self.volcheck+']')
        YG.debug('Time [%s'%takeTime)
        print('Total Golden Count [%s'%self.goldenCount+'] keepbuying[%s'%self.keepbuy+'] Volume[%s'%self.volcheck+']')
        print('Time [%s'%takeTime)
        


if __name__ == '__main__':
    
    dd=  GoldenSearchFromDB1()
    YG = YGGetCloseDB.YGGetCloseDB()
    YG.setProperties()
    YG.setLog()
    
#     ddf = str(159910)
#     Data = YG.getClosePriceFromDB(ddf)
#     print(dd.keepBuying(159910,Data,3))
#     print(dd.VolumeCheck(Data,3,10))
     
    dd.createSearchingDB(YG)



#     YG = YGGetCloseDB.YGGetCloseDB()
#     YG.setProperties()
#     codeNameCoast = YG.getCodeNameCoast()
#     
#     md = GoldenSearchFromDB1()
#     logger = logging.getLogger("YGLogger")
#     bld = BuyListDb.BuyListDB()
# #     bld.setProperties()
#     bld.createDatabase('../../Sqlite3/BuyList'+str(datetime.datetime.today().date())+'.db','BuyList')
# 
#     i=0
#     for code in range(len(codeNameCoast['Code'])):
#         code = codeNameCoast['Code'][code]
#         
#         md.Search(code,'2016-1-13','2016-02-25',YG,bld)
#         i+=1
# #         print('Code[',code,'] (',i,'/',len(codeNameCoast),')')
#         logger.debug('Code[ %s'%code+'] ( %s'%(i,)+'/ %s'%(len(codeNameCoast))+')')
#         print(' ',i,len(codeNameCoast))