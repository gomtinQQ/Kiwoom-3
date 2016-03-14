# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *
from PyQt4.QtCore import QVariant
import multiprocessing as mp
import re
from bs4 import BeautifulSoup
import time
import datetime
import sys,logging
sys.path.append('../')
sys.path.append('../Data')
import ExcelMake
import YGBuyListDB
from win32ras import GetConnectStatus



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

class Ui_Form(QAxWidget,mp.Process):
# class Ui_Form(QAxWidget):
    def __init__(self,**kwargs):
#         super().__init__()
#         mp.Process.__init__(self)
        super(Ui_Form, self).__init__(**kwargs)
        self.kiwoom = self.setControl('KHOPENAPI.KHOpenAPICtrl.1')
        self.connect(self, SIGNAL("OnEventConnect(int)"), self.OnEventConnect)
        self.connect(self, SIGNAL("OnReceiveMsg(QString, QString, QString, QString)"), self.OnReceiveMsg)
        self.connect(self, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self.OnReceiveTrData)
        
        self.connect(self, SIGNAL("OnReceiveChejanData(QString, int, QString)"),self.OnReceiveChejanData)
        self.connect(self, SIGNAL("OnReceiveRealData(QString, QString, QString)"),self.OnReceiveRealData)        
        self.btn_login()
        
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
#             code = self.kiwoom.connect(self.kiwoom, SIGNAL("OnEventConnect(int)"), self.OnEventConnect())
#             self.get10001Info()
            self.checkSendAndRealReg()
#             self.setReal()
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
            
    def OnReceiveRealData(self,sJongmokCode,sRealType,sRealData):
        print('===========RealData called===========[',datetime.datetime.now(),']')
        sRealData = str(sRealData)
        dd = sRealData.split(' ')
        df = str(dd[0]).split('    ')
#         print('sJongmokCode[',sJongmokCode,'] sRealType[',sRealType,'] sRealData[',sRealData,']')
        
        for index in range(len(df)):
            print(index,df[index])
        
        
    
    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList):
        
        print('===========ChejanData called===========')
        print('sGubun[',sGubun,'] nItemCnt[',nItemCnt,'] sFidList[',sFidList,']')
        chjang = self.dynamicCall('GetChejanData(QString)',9203)
        chjang1 = self.dynamicCall('GetChejanData(QString)',302)
        chjang2 = self.dynamicCall('GetChejanData(QString)',900)
        chjang3 = self.dynamicCall('GetChejanData(QString)',901)
        print(chjang,chjang1,chjang2,chjang3)
        
    def setReal(self):
        
        strScreenNo = "0002" #실시간 등록할 화면 번호 
        strCodeList  = "126700;000660;021080" #실시간 등록할 종목코드(복수종목가능 – “종목1;종목2;종목3;….”) 
        strFidList = "10" #실시간 등록할 FID(“FID1;FID2;FID3;…..”) EX) 10:현재가 11:전일대비 12:등락율 13:누적거래량 29:거래대금증감 32:거래비용
        strRealType ="1" #“0”, “1” 타입 
        
        ret = self.dynamicCall('SetRealReg(QString,QString,QString,QString)', strScreenNo,strCodeList,strFidList,strRealType)
        print('리얼타입 등록 :',ret)
        
    def get10001Info(self):
        ret = self.dynamicCall('SetInputValue(QString,QString)', "종목코드"    ,126700)
        ret = self.dynamicCall('CommRqData(QString,QString,int,QString)', "RQName"    ,  "opt10001"    ,  0   ,  "화면번호")
        self.connect(self, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self.OnReceiveTrData)

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
        sCode = str(code)      #주식코드
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
    def checkSendAndRealReg(self):
        

#         pool.apply_async(self.mpBSSet,(1,))

#         proc = mp.Process(name="set",target=self.mpBSSet)
#         proc.start()
#         print("END = = = = = = = = =  = = =")
        try:
             
            while(True):
             
                for index in range(len(code)):
                    rCode=self.addZeroToStockCode(str(code['Code'][index]))
                    print(rCode)
                    buySell = YG.getBuySell(rCode)
#                     if buySell=="N":
#                         self.sendOrder(rCode,"BUY")
#                         YG.buyStock(rCode,901,12000)                
                    if buySell =="Y":
                        self.sendOrder(rCode,"SELL")
                        YG.sellStock(rCode,902,12050)
                        '''세션클로스 주의'''
                time.sleep(1)
                 
        except Exception:
            print(Exception)
    def mpBSSet(self):
        try:
            print('1')
            YG = YGBuyListDB.YGGetDbData()
            print('2')
            YG.setProperties('../../Sqlite3/BuyList.db','BuyList')
            print('3')
            code = YG.getCodeNameForReaReg()
            print('4')
            while(True):
            
                for index in range(len(code)):
                    rCode=self.addZeroToStockCode(str(code['Code'][index]))
                    print(rCode)
                    buySell = YG.getBuySell(rCode)
#                     if buySell=="N":
#                         self.sendOrder(rCode,"BUY")
#                         YG.buyStock(rCode,901,12000)                
                    if buySell =="Y":
                        self.sendOrder(rCode,"SELL")
                        YG.sellStock(rCode,902,12050)
                        '''세션클로스 주의'''
                time.sleep(1)
                
        except Exception:
            print(Exception)
            
    def addZeroToStockCode(self,str):
        str=str.strip()
    
        if len(str.strip())<=6:
            while(len(str.strip())!=6):
                str=str[:0]+"0"+str[0:]
        return str

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    sys.exit(app.exec_())