# -*- coding: utf-8 -*-

import sqlite3
import sys,os
from _sqlite3 import OperationalError
from docutils.parsers.rst.directives import percentage
# sys.path.append('../')
sys.path.append('../Data')
sys.path.append('../DB')

import time,datetime

import traceback
import multiprocessing as mp
from SRC.Database import DBSet
from SRC.Database import YGBuyListDB

class RealAnalyse(DBSet.DBSet):

    def getSelectQuery(self,tableName,buySell,Time="",count="",interval="",multiplicationCheck="1"):
        '''set SimulatorTime if not,get the current Time'''

        if count=="":
            count=5
        count=int(count)

        if interval=="":
            interval=1
        interval=int(interval)
        self.tocount = 1


        
        currTime = self.getNowTime() 
        if Time is not "":
            currTime = str(Time)       #1분전 시간을 구한다
        beforeTime = self.pastAgo(currTime,interval)

        op=">"
        if buySell =="B" or buySell =="BUY":
            op = "<"
        if multiplicationCheck is "1":
            self.whereQuery = 'select StockCode,StockName from '+tableName+' where "' + \
                str(beforeTime) +'"'+op+'"' + str(currTime) + '"'

            self.getSelectQuery_proc(count, beforeTime ,interval,op)
            return self.whereQuery
        else:
            if tableName ==self.BuyListVolumeRotateTable:
#                 whereQuery= 'select StockCode,StockName from '+tableName+' where "' + \
#                 str(beforeTime) +'"*'+multiplicationCheck+''+op+'"' + str(currTime) +'"'
                whereQuery = 'select StockCode,StockName from {tableName} where "{beforeTime}"*{multiplicationCheck} {op} "{currTime}"'\
                .format(tableName=tableName,beforeTime=beforeTime,multiplicationCheck=multiplicationCheck,op=op,currTime=currTime)
                return whereQuery
            
            elif tableName == self.BuyListRelativeTable:
#                 whereQuery = 'select StockCode,StockName from {Relative} where {percentage}{op}(("{currTime}"-"{beforeTime}")/CAST ("{beforeTime}" AS REAL))*100.0'\
                whereQuery = 'select StockCode,StockName from {Relative} where {percentage}{op}(("{currTime}"-"{beforeTime}")/CAST ("{beforeTime}" AS REAL))*100.0'\
                .format(Relative=self.BuyListRelativeTable,currTime=str(currTime),beforeTime=str(beforeTime),percentage=multiplicationCheck,op=op) #percentage이상되는걸 고른다.
#                 print(whereQuery)
                return whereQuery
            
                
                
                

    def getSelectQuery_proc(self, count, Time,interval,op):
        '''
        get the update query set
        '''

        if self.tocount == count:
            self.tocount = 0
            return self.whereQuery

        else:
            currTime = Time
            beforeTime =self.pastAgo(currTime, interval)

            self.whereQuery = self.whereQuery + ' and "' + \
                str(beforeTime) +'"'+ op +'"' + str(currTime) + '"'

            self.tocount += 1
            self.getSelectQuery_proc(count, beforeTime,interval,op)

    def updateBuy(self,YG,buyListCode,cursor,conn):
        for i in range(len(buyListCode)):
            YG.updateBuy(buyListCode[i][0],cursor,conn)
        
    def checkCodeSet(self,YG,connection,Cursor,tableName,BS,multiplicationCheck="1",count="",interval=""):
        '''YG:업데이트할 클래스  , BS:BUY,SELL구분
        tableName : self.BuyListVolumeRotateTable일경우 거래량 테이블, self.BuyListRelativeTable 일경우 증가율 테이블
        multiplicationCheck : "1"이면 기본값,그외값이면 각 테이블 명칭에따라서 가격증가율또는 거래량은 곱셈이 됨.
        count : multiplicationCheck값이 기본값일때 몇분동안 체크할지 정한다.
        '''
        try:
            conn = connection
            cursor = Cursor

            if BS =="BUY":
                if count =="":
                    count=4
                if interval =="":
                    interval=1
                if multiplicationCheck is "1":
                    query = self.getSelectQuery(tableName, buySell=BS,count=count,interval=interval)
                    cursor.execute(query)
                    buyListCode= cursor.fetchall()
                    self.updateBuy(YG, buyListCode, cursor, conn)
                else:
#                     query = self.getSelectQuery(tableName,buySell=BS,Time="1303",multiplicationCheck=multiplicationCheck,count=count,interval=interval)
                    query = self.getSelectQuery(tableName,buySell=BS,multiplicationCheck=multiplicationCheck,count=count,interval=interval)
#                     print(query)
                    cursor.execute(query)
                    buyListCode= cursor.fetchall()
                    return buyListCode

            elif BS == "SELL":

                if count =="":
                    count=3
                if interval =="":
                    interval=1

                if multiplicationCheck is "1":
                    query = self.getSelectQuery(tableName, buySell=BS,count=count,interval=interval)
    
                    cursor.execute(query)
                    buyListCode= cursor.fetchall()
    #                 print(query)
                    for i in range(len(buyListCode)):
                        YG.updateSell(buyListCode[i][0],cursor,conn)
    #                     print(buyListCode[i][0])
                else:
#                     query = self.getSelectQuery(tableName,buySell=BS,Time="1303",multiplicationCheck=multiplicationCheck,count=count,interval=interval)
                    query = self.getSelectQuery(tableName,buySell=BS,multiplicationCheck=multiplicationCheck,count=count,interval=interval)
                    cursor.execute(query)
                    print(query)
                    buyListCode= cursor.fetchall()
                    return buyListCode
                    
                    
                    
            elif BS == "END":

                query = 'select StockCode from '+tableName+' where "BUYSELL"="Y" or "BUYSELL"="B"'
                cursor.execute(query)
                buyListCode = cursor.fetchall()

                print("영업종료하자")
                YG.debug("영업종료하자")
                try:
                    for i in range(len(buyListCode)):
                        YG.updateSell(buyListCode[i][0],cursor,conn)
                except :
                    YG.tracebackLog()


            else :
                print('Select correctly Buy or Sell ')

        except :
            self.tracebackLog()


    def setDB(self,DB):
        self.DB= DB
    def setConfig(self,config):
        self.config=config

    def gogo(self,Test=""):

        YG = YGBuyListDB.YGGetDbData()
        YG.setProperties(self.DB,YG.BuyListRelativeTable)

#         conn = sqlite3.connect(self.BuyListDBToday)
        conn = sqlite3.connect(YG.BuyListDBYesterday)
        cursor = conn.cursor()
        self.setLog(__name__)
        mode="Real"
        if Test is not None:
            mode=Test

        if mode =="Real":

            while(True):
                print("901분 부터 시작합니다.. [현재시각 :",self.getNowTime(),"]")
                if self.getNowTime()=="0901" or self.getNowTime() =="901":
                    break
                else:
                    time.sleep(1)

            print("Real data 분석 시작 !!!!!!!!!!!!!!!!!!!!!!!!!")
            while(True):
                try:
                    self.checkCodeSet(YG,conn,cursor, self.BuyListRelativeTable,'BUY' )
                    self.checkCodeSet(YG,conn,cursor, self.BuyListVolumeRotateTable,'BUY' )

                    self.checkCodeSet(YG,conn,cursor, self.BuyListRelativeTable,'SELL' )
                    self.checkCodeSet(YG,conn,cursor, self.BuyListVolumeRotateTable,'SELL' )

                    if self.getNowTime() == "1449":
                        self.checkCodeSet(YG,conn,cursor,self.BuyListTable,'END')
                        break

                    time.sleep(0.5)
                except Exception:
                    self.tracebackLog()
                    print("realData Analyzer종료함.")
#                     break
                    continue
            print("장 종료되었음.")
        elif mode=="Test":

            while(self.getNowTime()!= "1500"):
                try:
                    self.checkCodeSet(YG,conn,cursor, self.BuyListRelativeTable,'BUY')
                    self.checkCodeSet(YG,conn,cursor, self.BuyListVolumeRotateTable,'BUY')

                    time.sleep(0.5)
                except Exception:
                    self.tracebackLog()
                    break
                    continue
        elif mode =="RealPart2":
            
            print("RealPart2 분석 시작 !!!!!!!!!!!!!!!!!!!!!!!!!")
            
            while(self.checkDate() is not True):
                time.sleep(2)
                continue
            
            while(True):
#                 print("분석시작 ")
                try:
                    #살것 체크###########
                    buyListCode = self.checkCodeSet(YG,conn,cursor, self.BuyListVolumeRotateTable,'BUY' ,multiplicationCheck="5",count=1,interval=1 ) #1분전 상황보다 거래량이 5배이상 증가 ?
                    buyListCode2 = self.checkCodeSet(YG,conn,cursor, self.BuyListRelativeTable,'BUY',multiplicationCheck="0.5",count=1,interval=1 ) #1분전보다 가격 0.5프로 이상 증가?
                     
                    
#                     if buyListCode is not None and buyListCode2 is not None:
                    if buyListCode[0] is not None and buyListCode2[0] is not None:
                        if len(buyListCode)  !=0 and len(buyListCode2) != 0:
                            if len(buyListCode)>len(buyListCode2):
                                bc = buyListCode2
                            else :
                                bc = buyListCode
                            for i in range(len(bc)):
                                if buyListCode2[i][0] in buyListCode[i]:
                                    msg ='buying signal! {code}'.format(code=buyListCode2[i][0])
                                    self.debug(msg)
                                    YG.updateBuy(buyListCode[i][0],cursor,conn)

                    #팔것 체크###########
                    
                    BuyListCodeFotime = self.selectSellingQueryCheck(YG,conn,cursor,self.BuyListRelativeTable)
                    
#                     buyListCode = self.checkCodeSet2(YG,conn,cursor, self.BuyListRelativeTable,'SELL',multiplicationCheck=2 )    #산것보다 가격이 2프로이상 증가?
                    if BuyListCodeFotime[0][0] is not None and BuyListCodeFotime[0][1] is not None:
                        self.checkCodeSet2(YG, conn, cursor, self.BuyListRelativeTable,'SELL', BuyListCodeFotime)#산것보다 가격이 2프로이상 증가?

                    if self.getNowTime() == "1448" or self.getNowTime() == "1449" or self.getNowTime() == "1447":
                        self.checkCodeSet(YG,conn,cursor,self.BuyListTable,'END')
                        break

                    time.sleep(0.5)
                except Exception:
                    self.tracebackLog()
                    print("realData Analyzer에러남")
#                     break
                    continue
            print("장 종료되었음.")

    def selectSellingQueryCheck(self,YG,conn,cursor,tableName):
        
        '''buySell="Y"중에서 bstime과 stockCode를 가져온다'''
        
        '''select A.StockCode,B.BSTime \
        from Relative A join BuyList B on A.StockCode=B.StockCode\
        where B.BUYSELL="Y" '''
        
        query ='select A.StockCode,B.BSTime \
        from {tableName} a join BuyList B on A.StockCode=B.StockCode\
        where B.BUYSELL="{buySell}"'.format(tableName=tableName,buySell="Y");
        try:
#         print(query)
            cursor.execute(query)
            buyListCode= cursor.fetchall()
        except :
            self.tracebackLog()
        
        return buyListCode
#         print(buyListCode)
    
    def checkDate(self):
        
        now = datetime.datetime.now()
        
        
        start_time = datetime.datetime(now.year,now.month,now.day,9,10)
        
        checkStart = False
        if now>start_time:
            checkStart = True
        print('현재시각 . [',now,'] start symbol [',checkStart,']')
        return checkStart
    
    def checkCodeSet2(self,YG,conn,cursor,tableName,BS,multiplicationCheck ):
        #산것보다 가격이 2프로이상 증가?
        try:
            if BS=='SELL':
                if multiplicationCheck is not None:
                    for i in range(len(multiplicationCheck)):
                        stockCode = multiplicationCheck[i][0]   #code
                        foTime = multiplicationCheck[i][1]      #산 시각
                        nowTime = self.getRealTime()
#                         nowTime="901"
                        query ='select "{foTime}","{nowTime}" from {tableName} where StockCode="{stockCode}"'\
                        .format(tableName=tableName,foTime=foTime,stockCode=stockCode,nowTime=nowTime)
                        
                        cursor.execute(query)
                        
                        info = cursor.fetchall()
                        msg = "queryResult is {info} query [{query}]".format(info=info,query=query)
                        self.debug(msg)
                        if info[0][0] !='None' and info is not None and info[0][1] !='None':
                            
                            buyPrice = float(info[0][0]) #산 갸격
                            nowPrice= float(info[0][1]) #현재 갸격
                            msg = '산가격 :{buyPrice} 현재가격:{nowPrice}'.format(buyPrice=buyPrice,nowPrice=nowPrice)
                            self.debug(msg)
                            if ((nowPrice-buyPrice)/buyPrice) *100 <-3:
                                print('가격이 3프로이상하락 하락율 :',((nowPrice-buyPrice)/buyPrice)*100)
                                msg = '가격이 3프로이상하락 하락율 : {msg}'.format(msg = ((nowPrice-buyPrice)/buyPrice)*100)
                                self.debug(msg)
                                YG.updateSell(stockCode, cursor, conn)
                            
                            elif ((nowPrice-buyPrice)/buyPrice)*100>2:
                                print('가격이 2프로이상증가 증가율 :',((nowPrice-buyPrice)/buyPrice)*100)
                                msg = '가격이 2프로이상증가 증가율 : {msg}'.format(msg = ((nowPrice-buyPrice)/buyPrice)*100)
                                self.debug(msg)
                                YG.updateSell(stockCode, cursor, conn)
                        else:
                            msg = 'info : [{info}] query : [{query}]'.format(info=info,query=query)
                            YG.debug(msg)
                        
                        
                            
        except :
            self.tracebackLog()
                    
            
        
        
            
if __name__ == '__main__':
    ra = RealAnalyse()

    YG = YGBuyListDB.YGGetDbData()
#     YG.setProperties(YG.BuyListDBToday,YG.BuyListRelativeTable)

    ra.setDB(YG.BuyListDBYesterday)
#     ra.setDB(YG.BuyListDBToday)
    proc = mp.Process(target=ra.gogo,args=["RealPart2",])
    proc.start()

#     ra.start()
#     print(ra.getSelectQuery('tableName','BUY',interval=60,count=1))
