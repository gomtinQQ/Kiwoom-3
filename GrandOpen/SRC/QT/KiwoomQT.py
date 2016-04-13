# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *
from PyQt4.QtCore import QVariant
import re
import traceback
from bs4 import BeautifulSoup
import time
import datetime
import sys,logging
from ipyparallel.controller.sqlitedb import sqlite3
sys.path.append("../")
sys.path.append("../Database")
import statistics
import multiprocessing as mp
from win32ras import GetConnectStatus
from SRC.Database import YGBuyListDB
from SRC.Database.Analyzer import RealDataAnalyzer



try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QAxWidget):
    def __init__(self,YG):
        super().__init__()
        self.kiwoom = self.setControl('KHOPENAPI.KHOpenAPICtrl.1')
        self.connect(self, SIGNAL("OnEventConnect(int)"), self.OnEventConnect)
        self.connect(self, SIGNAL("OnReceiveMsg(QString, QString, QString, QString)"), self.OnReceiveMsg)
        self.connect(self, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self.OnReceiveTrData)
        
        self.connect(self, SIGNAL("OnReceiveChejanData(QString, int, QString)"),self.OnReceiveChejanData)
        self.connect(self, SIGNAL("OnReceiveRealData(QString, QString, QString)"),self.OnReceiveRealData)        
#         self.YG = YGBuyListDB.YGGetDbData()
        self.YG=YG
        
        
        
#         self.YG.setProperties(self.YG.BuyListDBYesterday,self.YG.BuyListTable)
#         self.YG.setProperties(self.YG.BuyListDBToday,self.YG.BuyListTable)
#         self.YG.setLog()
        self.btn_login()
        self.acumulativeVolume={} #누적거래량 변수
        self.perPast={}
        self.pastMinute = datetime.datetime.now().minute #현재 분
        self.timeVal={}
        
        print("=============initializing completed============================")
#         ra = RealDataAnalyzer.RealAnalyse()
#         proc = mp.Process(target=ra.gogo,args=(self.YG,))
#         proc.start()

        
    def btn_login(self):        
        ret = self.dynamicCall("CommConnect()") 
        
    def OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        
        print('===========OnReceiveMSG called===========')
        print('sScrNo[',sScrNo,'] sRQName[', sRQName,'] sTrCode[', sTrCode,'] sMsg[', sMsg,']')
    
    def getConnectState(self):
        ret = self.dynamicCall('GetConnectState()')
        print("Login successs")
        return ret

    def btn_Quit(self):
        self.dynamicCall("CommTerminate()")
        sys.exit()
    
    def OnEventConnect(self, nErrCode):
        if nErrCode == 0:
            print("서버에 연결 되었습니다...")
            ra = RealDataAnalyzer.RealAnalyse()
            ra.setDB(YG.BuyListDBYesterday)
            proc = mp.Process(target=ra.gogo)
            proc.start()
#             code = self.kiwoom.connect(self.kiwoom, SIGNAL("OnEventConnect(int)"), self.OnEventConnect())
#             self.get10001Info()
            self.setReal()
#             self.checkSendAndRealReg()
#             self.sendOrder()
        else:
            print("서버 연결에 실패 했습니다...")
             
            
    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSPlmMsg):
        
        print('===========TRData called===========')
        print('sScrNo[',sScrNo,'] sRQName[' ,sRQName,'] sTrCode[', sTrCode,'] sRecordName[', sRecordName,'] sPreNext[', sPreNext,'] nDataLength[', nDataLength,'] sErrorCode[', sErrorCode,'] sMessage[', sMessage,'] sSPlmMsg[', sSPlmMsg,']')
        if sTrCode == "opt10001":
            ItemName = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "종목명")
            CurrCoast = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "현재가")
            volume = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "거래량")
            
            print(ItemName,CurrCoast,volume)
            
    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList):
        print('===========ChejanData called===========')
        print('sGubun[',sGubun,'] nItemCnt[',nItemCnt,'] sFidList[',sFidList,']')
        chjang = self.dynamicCall('GetChejanData(QString)',9203)
        chjang1 = self.dynamicCall('GetChejanData(QString)',302)
        chjang2 = self.dynamicCall('GetChejanData(QString)',900)
        chjang3 = self.dynamicCall('GetChejanData(QString)',901)
        print(chjang,chjang1,chjang2,chjang3)
        
    def OnReceiveRealData(self,sJongmokCode,sRealType,sRealData):
        
        

#         print('===========RealData called===========[',datetime.datetime.now(),']')
        sRealData = str(sRealData)
#         print('sJongmokCode[',sJongmokCode,'] sRealType[',sRealType,'] sRealData[',sRealData,']')
        
#         Fid = '10;31;29;26;15;12' #현재가,회전율,거래대금증감,전일거래량대비,거래량 체결량 , 등락율
        CurrPrice = self.dynamicCall('GetCommRealData(QString, int )',sRealType,10)
        VolumeRotate = self.dynamicCall('GetCommRealData(QString, int )',sRealType,31)
        RelativeVolume = self.dynamicCall('GetCommRealData(QString, int )',sRealType,26)
        
        yester = self.dynamicCall('GetCommRealData(QString, int )',sRealType,11)
        
        relative = self.dynamicCall('GetCommRealData(QString, int )',sRealType,12)
        
        volume= self.dynamicCall('GetCommRealData(QString, int )',sRealType,15)
        
#         print(volume) #체결량이랑 거래량인데 어떻게 들어오는지 확인해야함 그래서 거래량만 파싱해야함.!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        
        try:
            self.acumulativeVolume[sJongmokCode]
            self.perPast[sJongmokCode]
        except :
            self.acumulativeVolume[sJongmokCode]=0
            self.perPast[sJongmokCode]= str(self.pastMinute)
        
        try:
            self.acumulativeVolume[sJongmokCode]+=int(volume)
        except :
            print('거래량 에러',volume)
        self.currMinute = datetime.datetime.now().minute
        
        tim = datetime.datetime.now()
        hour = str(tim.hour)
        minute = str(self.pastMinute)
        
        if self.perPast[sJongmokCode] !=None:
            minute =str(self.perPast[sJongmokCode])
            
        if len(minute)<2:
            minute='0'+minute
        foTime = hour+minute
        
        self.timeVal[sJongmokCode] = foTime,self.acumulativeVolume[sJongmokCode]
        if self.perPast[sJongmokCode] ==None:
            self.perPast[sJongmokCode]=minute
#         if self.pastMinute != self.currMinute :
#         print(sJongmokCode, self.perPast[sJongmokCode],self.currMinute)
        if self.perPast[sJongmokCode] != str(self.currMinute):
            print(sJongmokCode,self.acumulativeVolume[sJongmokCode],self.perPast[sJongmokCode])
            self.perPast[sJongmokCode] = str(self.currMinute)
            
            self.YG.updateVolumeCode(sJongmokCode,self.acumulativeVolume[sJongmokCode],self.timeVal[sJongmokCode])
            self.YG.updateRelativeCode(sJongmokCode,CurrPrice,self.timeVal[sJongmokCode])
            
            self.acumulativeVolume[sJongmokCode] =0 #거래량 다시 초기화
            self.timeVal[sJongmokCode] = None
            
        self.checkBuyOrSell(foTime,CurrPrice)
        
#         
#         if float(VolumeRotate) > 6 and float(relative) > 6:
# #             self.YG.debug('종목코드[%s'%sJongmokCode+']@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
# #             self.YG.updateCode(sJongmokCode,relative,VolumeRotate)
#             
#             self.YG.updateRelativeCode(sJongmokCode,relative)
#             self.YG.updateVolumeCode(sJongmokCode,VolumeRotate)
#             print('종목코드[%s'%sJongmokCode+'] 현재가[%s'%CurrPrice+'] Rotate[%s'%VolumeRotate+'] 전일대비[%s'%yester+'] 등락율[%s'%relative+']')
#             self.YG.debug('종목코드[%s'%sJongmokCode+'] 현재가[%s'%CurrPrice+'] Rotate[%s'%VolumeRotate+'] 전일대비[%s'%yester+'] 등락율[%s'%relative+']')
#             
            
#         self.YG.debug('종목코드[%s'%sJongmokCode+'] 현재가[%s'%CurrPrice+'] Rotate[%s'%VolumeRotate+'] 전일대비[%s'%yester+'] 등락율[%s'%relative+']')
#         print('종목코드[%s'%sJongmokCode+'] 현재가[%s'%CurrPrice+'] Rotate[%s'%VolumeRotate+'] 전일대비[%s'%yester+'] 등락율[%s'%relative+']')
        
    
        
    
        
    def setReal(self):
        
        strScreenNo = "0002" #실시간 등록할 화면 번호 
#         strCodeList  = "126700;000660;021080" #실시간 등록할 종목코드(복수종목가능 – “종목1;종목2;종목3;….”)


#         print(DB,Table)
        code = self.YG.getCodeNameForReaReg()
        strCodeList = "" 
        try: 
            for index in range(len(code)):
                rCode = self.addZeroToStockCode(str(code['Code'][index]))
                strCodeList +=rCode+';'
                
            strCodeList = strCodeList[:len(strCodeList)-1]  #remove last character = ';'
            print(strCodeList)
        except Exception:
            traceback.print_exc()
        
        
#         strFidList = "10" #실시간 등록할 FID(“FID1;FID2;FID3;…..”) EX) 10:현재가 11:전일대비 12:등락율 13:누적거래량 29:거래대금증감 32:거래비용
        strFidList = "9001;10;13" #code,currPrice,acumulVolume
        strRealType ="1" #“0”, “1” 타입 
        
        ret = self.dynamicCall('SetRealReg(QString,QString,QString,QString)', strScreenNo,strCodeList,strFidList,strRealType)
        print('리얼타입 등록 :',ret)
        

    def checkBuyOrSell(self,time,CurrPrice):
        
#         self.YG = YGBuyListDB.YGGetDbData()
#         today = datetime.datetime.today().date()
#         oneDay = datetime.timedelta(days=1)
#         
#         YESTERDAY= str( today - oneDay) 
#         DB = '../../Sqlite3/BuyList'+YESTERDAY+'.db'
#         Table='BuyList'
#         
#         self.YG.setProperties(DB,Table)
        try:
            
#             while(True):
            stockCodeList = self.YG.getBuySell()
            
            for i in range(len(stockCodeList)):
                stockCode = stockCodeList[i][0]
                
                if str(stockCodeList[i][1]) =="B":
                    self.YG.buyStock(stockCode,time,CurrPrice)#dblogging
                    self.sendOrder(stockCode,"BUY")#sendOrder
                
                elif str(stockCodeList[i][1]) =="S":
                    self.YG.sellStock(stockCode,time,CurrPrice)#dblogging
                    self.sendOrder(stockCode,"SELL")#sendOrder
                
                
#                 for index in range(len(code)):
#                     rCode=self.addZeroToStockCode(str(code['Code'][index]))
#                     buySell = self.YG.getBuySell(rCode)
#                     if buySell=="N":
#                         self.sendOrder(rCode,"BUY")
#                         self.YG.buyStock(rCode,901,12000)                
#                     if buySell =="Y":
#                         self.sendOrder(rCode,"SELL")
#                         self.YG.sellStock(rCode,905,236200)
#                 time.sleep(5)
                
        except Exception:
            traceback.print_exc()
            
    def sendOrder (self,code,Position):
        
        print('SendOrder Called! Position :',Position )
        ACCOUNT_CNT = self.dynamicCall('GetLoginInfo("ACCOUNT_CNT")')
        ACC_NO = self.dynamicCall('GetLoginInfo("ACCNO")')
        sRQName  = "주식주문" # 사용자 구분 요청 명 
        sScreenNo = "0107" #화면번호[4]
        ACCNO=ACC_NO.replace(';','')    #계좌번호
        nOrderType = 1      #1신규매수 2신규매도 3매수취소 4매도취소 5매수정정 6매도정정
        if Position == "SELL":
            nOrderType = 2
        sCode = self.addZeroToStockCode(str(code))      #주식코드
        nQty  = 10          #주문수량
        nPrice  = 0         #주문단가
        sHogaGb  = "03"   #0:지정가, 3:시장가, 5:조건부지정가, 6:최유리지정가, 7:최우선지정가, 10:지정가 IOC, 13:시장가IOC, 16:최유리IOC, 20:지정가FOK, 23:시장가FOK, 26:최유리FOK, 61:시간외 단일가매매, 81:시간외종가
        sOrgOrderNo  = "" #원주문번호
        Order = self.dynamicCall('SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)', [sRQName,sScreenNo , ACCNO, nOrderType, sCode, nQty,nPrice,sHogaGb,sOrgOrderNo])
        print('End!! ',sCode)
        
        '''지정가 매수 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 1, “000660”, 10, 48500, “0”, “”);     '''
        '''시장가 매수 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 1, “000660”, 10, 0, “3”, “”);         '''
        '''매수 정정 -  openApi.SendOrder(“RQ_1”,“0101”, “5015123410”, 5, “000660”, 10, 49500, “0”, “1”);      '''
        '''매수 취소 -  openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 3, “000660”, 10, “0”, “2”);            '''
            
    def addZeroToStockCode(self,str):
        str=str.strip()
    
        if len(str.strip())<=6:
            while(len(str.strip())!=6):
                str=str[:0]+"0"+str[0:]
        return str

if __name__ == "__main__":
    

        
    
    YG = YGBuyListDB.YGGetDbData()
    YG.setProperties(YG.BuyListDBYesterday,YG.BuyListTable)
    YG.setLog()
#     YG.setQueue(q)
    
        
#     ra = RealDataAnalyzer.RealAnalyse()
#     ra.setDB(YG.BuyListDBYesterday)
#     proc = mp.Process(target=ra.gogo)
#     proc.start()
#     ra.gogo(YG)
    
#     d.setYG(YG)
#     d.start() 
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form(YG)
    sys.exit(app.exec_())