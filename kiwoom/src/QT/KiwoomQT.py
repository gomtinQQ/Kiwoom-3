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
        self.btn_login()
        
        
        
#         print(code)
#         self.action_New.triggered.connect(self.get10001Info())

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
            self.get10001Info()
#             print(code)
        else:
            print("서버 연결에 실패 했습니다...")
             
            
    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSPlmMsg):
        
        print(sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSPlmMsg)
        if sTrCode == "opt10001":
            ItemName = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "종목명")
            CurrCoast = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "현재가")
            print(ItemName,CurrCoast)
            
    
    def get10001Info(self):
        
        
        ret = self.dynamicCall('SetInputValue(QString,QString)', "종목코드"    ,126700)
        ret = self.dynamicCall('CommRqData(QString,QString,int,QString)', "RQName"    ,  "opt10001"    ,  0   ,  "화면번호")
        self.connect(self, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self.OnReceiveTrData)
    

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.get10001Info()
#     Form.show()
    sys.exit(app.exec_())

