# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *
from PyQt4.QtCore import QVariant
import re
from bs4 import BeautifulSoup
import time
import sys
sys.path.append('../')
import ExcelMake
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

class Ui_Form(QAxWidget):
    def __init__(self):
        super().__init__()
        self.kiwoom = self.setControl('KHOPENAPI.KHOpenAPICtrl.1')
        self.connect(self, SIGNAL("OnEventConnect(int)"), self.OnEventConnect)
        self.connect(self, SIGNAL("OnReceiveMsg(QString, QString, QString, QString)"), self.OnReceiveMsg)
        self.connect(self, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self.OnReceiveTrData)
        
        self.connect(self, SIGNAL("OnReceiveChejanData(QString, int, QString)"),self.OnReceiveChejanData)
        
        self.connect(self, SIGNAL("OnReceiveRealData(QString, QString, QString)"),self.OnReceiveRealData)
        
        self.btn_login()
        
    def btn_login(self):        
        ret = self.dynamicCall("CommConnect()") 
        
    
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
            self.setReal()
#             self.sendOrder()
        else:
            print("서버 연결에 실패 했습니다...")
             
            
    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSPlmMsg):
        
        print(sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSPlmMsg)
        if sTrCode == "opt10001":
            ItemName = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "종목명")
            CurrCoast = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "현재가")
            volume = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "거래량")
            
            print(ItemName,CurrCoast,volume)
            
    def OnReceiveRealData(self,sJongmokCode,sRealType,sRealData):
        print(sJongmokCode,sRealType,sRealData)
    
    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList):
        
        print('wef')
        print(sGubun,nItemCnt,sFidList)
        print(self.GetChjanData(9203),self.GetChjanData(9203),self.GetChjanData(302),self.GetChjanData(900),self.GetChjanData(901))
        
    def setReal(self):
        ret = self.dynamicCall('SetRealReg(QString,QString,QString,QString)', "0001"    ,  "126700"    ,  "10",  "0")
        ret = self.connect(self, SIGNAL("OnReceiveRealData(QString, QString, QString)"), self.OnReceiveRealData)
        print(ret)
        
    def get10001Info(self):
        ret = self.dynamicCall('SetInputValue(QString,QString)', "종목코드"    ,126700)
        ret = self.dynamicCall('CommRqData(QString,QString,int,QString)', "RQName"    ,  "opt10001"    ,  0   ,  "화면번호")
        self.connect(self, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self.OnReceiveTrData)

    def sendOrder (self):
        ACCOUNT_CNT = self.dynamicCall('GetLoginInfo("ACCOUNT_CNT")')
        ACC_NO = self.dynamicCall('GetLoginInfo("ACCNO")')
        print(ACCOUNT_CNT)
        print(ACC_NO)
        ACCNO=ACC_NO.replace(';','')
        Order = self.dynamicCall('SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)', ["주식주문", "0107", ACCNO, 1, "126700", "1",0, "3",""])
        self.connect(self, SIGNAL("OnReceiveChejanData(QString, int, QString)"), self.OnReceiveChejanData)
        print('Order',Order)
        #시장가 매수 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 1, “000660”, 10, 0, “3”, “”); 
    

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    sys.exit(app.exec_())

