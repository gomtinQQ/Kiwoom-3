# -*- coding: utf-8 -*-
import datetime,time
import sys,traceback

from SRC.Database import YGGetCloseDB,BuyListDb,YGBuyListDB
from SRC.Graph import DrawGraph
import configparser
import logging
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
                if str(dd['Foreign'][index]) == 'nan':
                    print('None Foreign! ' ,code)
                Foreign = int(dd['Foreign'][index])
                if str(dd['Company'][index]) == 'nan':
                    print('None Company! ' ,code)
#                 print(dd['Company'][index])
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
#             YG.debug(traceback.print_exc())
            print(traceback.print_exc())
    
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
#             YG.debug(traceback.print_exc())
            print(traceback.print_exc())
        except Exception as a:
#             YG.debug(traceback.print_exc())
            print(traceback.print_exc())
            
    def VolumeCheck(self,Data,standard,condition):
        '''가장 최근일을 기준으로 몇일동안 거래량증가했는지 day로 나타냄'''
        '''ex)최근standard 일동안의 거래량이 condition거래량보다 높은지 확인.'''
        '''높으면 거래량 급증이라 판단, return true 그렇지안으면 false'''
        '''ex) standard=3, condition=20  3일동안의 거래량>20일동안의 거래량'''
        
        
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
        
        
    def Search(self,Code,end,YG,bld,DBLog,name,timeOut=""):
        Data = YG.getClosePriceFromDB(str(Code))
        
        if len(Data) <20: #거래일이 20일미만인건 걍 보내주자.
            return
        
        Data['ma5']=DrawGraph.movingAverage(Data['Close'],5)
        Data['ma20']=DrawGraph.movingAverage(Data['Close'],20)
        Data['ma60']=DrawGraph.movingAverage(Data['Close'],60)
        
        Data['Golden_20_5']=Data['ma5']-Data['ma20']
        
        
        Gold = self.Golden(Data)
        if Gold == None :   #골든크로스 안뜸
            return
        
        try:
            dd =Gold.to_datetime()
            
            date_fmt='%Y-%m-%d'
            end =datetime.datetime.strptime(end,date_fmt)
            
            if end<dd and self.keepBuying(Code,Data,10,FOREIGNER=True,COMPANY=False):
                
                print('Foreigner keepBuying~ Code',Code,' When: ',dd )
                self.goldenCount+=1
                self.keepbuy+=1
                YG.debug('keepBuying ~ [%s'%Code+'] DATE [ %s'%dd+']')
                
                if DBLog:
                    bld.insertGold(str(Code),name)
                    
            elif end<dd and self.keepBuying(Code,Data,10,COMPANY=True,FOREIGNER=False):
                print('Company keepBuying~ Code',Code,' When: ',dd )
                self.goldenCount+=1
                self.keepbuy+=1
                YG.debug('keepBuying ~ [%s'%Code+'] DATE [ %s'%dd+']')
                
                if DBLog:
                    bld.insertGold(str(Code),name)

            elif end<dd and self.keepBuying(Code,Data,3,COMPANY=True,FOREIGNER=True):
                print('Both keepBuying~ Code',Code,' When: ',dd )
                self.goldenCount+=1
                self.keepbuy+=1
                YG.debug('keepBuying ~ [%s'%Code+'] DATE [ %s'%dd+']')
                
                if DBLog:
                    bld.insertGold(str(Code),name)
                
            elif end<dd and self.VolumeCheck(Data,3,20):
                
#                 print('Volume!~ Code',Code,' When: ',dd ,end="")
                print('Volume!~ Code',Code,' When: ',dd )
                self.goldenCount+=1
                self.volcheck+=1
                YG.debug('Volume!~ [%s'%Code+'] DATE [ %s'%dd+']')
                
                if DBLog:
                    bld.insertGold(str(Code),name)
        
        except Exception as a :
            print(traceback.print_exc())

    def createSearchingDB(self,YG):
        
        start_time = time.time()
        codeNameCoast = YG.getCodeNameCoast()
        
        
        BuyListDb.BuyListDB().createDefaultDB()
        bld = YGBuyListDB.YGGetDbData()
        bld.setProperties(bld.BuyListDBToday,bld.BuyListTable)
        i=0
        self.goldenCount = 0
        self.keepbuy=0
        self.volcheck=0
        DBLog=True
        print("DB LOGGING [",DBLog,"]")
        for index in range(len(codeNameCoast['code'])):
            code = codeNameCoast['code'][index]
            name = codeNameCoast['name'][index]
            
            self.Search(code,'2016-02-25',YG,bld,DBLog,name)
            i+=1
            YG.debug('Code[%s'%code+'] ( %s'%(i,)+'/ %s'%(len(codeNameCoast))+')')
        takeTime=time.time()-start_time
        YG.debug('Total Golden Count [%s'%self.goldenCount+'] keepbuying[%s'%self.keepbuy+'] Volume[%s'%self.volcheck+']')
        YG.debug('Time [%s'%takeTime)
        print('Total Golden Count [%s'%self.goldenCount+'] keepbuying[%s'%self.keepbuy+'] Volume[%s'%self.volcheck+']')
        print('Time [%s'%takeTime)
        
def gogo(config):
    dd=  GoldenSearchFromDB1()
    YG = YGGetCloseDB.YGGetCloseDB(config)
    YG.setProperties()
    YG.setLog()     
    dd.createSearchingDB(YG,config)
    

if __name__ == '__main__':
    
    dd=  GoldenSearchFromDB1()
    YG = YGGetCloseDB.YGGetCloseDB()
    YG.setProperties()
    YG.setLog()
    
     
    dd.createSearchingDB(YG)


