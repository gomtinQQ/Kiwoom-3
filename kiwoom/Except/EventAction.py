# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *
from PyQt4.QtCore import QVariant
import sys
import re


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
class EAction:
    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSPlmMsg):
            if sTrCode == "OPT10001":
                
                cnt = self.dynamicCall('GetRepeatCnt(QString, QString)', sTrCode, sRQName)
                ItemName = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "종목명")
                CurrCoast = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "현재가")
                self.codelist = self.GetCodeListByMarket(10)
                
                totalItem = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "상장종목수")
                self.textEdit.append("카운트 :" +str(cnt))
                self.textEdit.append("창번호: "+sScrNo)
                self.textEdit.append("종목명: "+ItemName.strip())
                self.textEdit.append("현재가: "+CurrCoast.strip())
                
                self.getTotalInfo()
                 
            if sTrCode == "OPT20003":
                cnt = self.dynamicCall('GetRepeatCnt(QString, QString)', sTrCode, sRQName)
                ItemName = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "종목명")
                CurrCoast = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "현재가")
                
                totalItem = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "상장종목수")
                ItemCode = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "종목코드")
                self.textEdit.append("============================================")
                self.textEdit.append(totalItem)
                self.textEdit.append(ItemCode)
                if ItemCode.strip()=='101':  #코스닥
                    self.lineEdit_10.setText(totalItem.strip())
                elif ItemCode.strip()=='001':
                    self.lineEdit_9.setText(totalItem.strip())
    def btn_clicked3(self):
            Code = self.lineEdit.text().strip()
            ret = self.dynamicCall('SetInputValue(QString, QString)', "종목코드", Code)
            ret = self.dynamicCall('CommRqData(QString, QString, int, QString)', "주식기본정보", "OPT10001", 2, "0101")
             
    def getTotalInfo(self):    
        ret = self.dynamicCall('SetInputValue(QString, QString)', "업종코드", '101')
        ret = self.dynamicCall('CommRqData(QString, QString, int, QString)', "주식기본정보", "OPT20003", 2, "0102")
        ret = self.dynamicCall('SetInputValue(QString, QString)', "업종코드", '001')
        ret = self.dynamicCall('CommRqData(QString, QString, int, QString)', "주식기본정보", "OPT20003", 2, "0101")
    #     def getKospiInfo(self):
    #         ret = self.dynamicCall('SetInputValue(QString, QString)', "업종코드", '001')
    #         ret = self.dynamicCall('CommRqData(QString, QString, int, QString)', "주식기본정보", "OPT20003", 0, "0101")
    
    
        
    def btn_info(self):
        ACCOUNT_CNT = self.dynamicCall('GetLoginInfo("ACCOUNT_CNT")')
        ACC_NO = self.dynamicCall('GetLoginInfo("ACCNO")')
        print(ACC_NO)
        ACCNO = re.sub(';','', ACC_NO)
        self.textEdit.append("보유 계좌수: "+ACCOUNT_CNT + " " + "계좌번호: "+ACCNO)
        self.lineEdit_2.setText(ACCNO)
        self.excel = ExcelMakeBak.ExcelCode()          #클릭때마다 객체가생성됨.
        self.excel.addToExcel(self.codelist)
        self.mylist =self.codelist.split(';')
        
        
        
        
        for a in self.mylist:
            self.excel.addToExcelCodeName(self.GetMasterCodeName(a))
            
        print(ACCNO)
    
    
    def GetChjanData(self, nFid):
        chjang = self.dynamicCall('GetChejanData(QString)', nFid)
        return chjang
    
    def  GetCodeListByMarket(self, sMarket):
        codelist =self.dynamicCall('GetCodeListByMarket(QString)',sMarket)
        return codelist 
    
    
    def btn_SendOrder(self):
        HogaGb = self.comboBox.currentText()[0:2].strip()
        Type = int(self.comboBox_2.currentText()[0:1].strip())
        Code = self.lineEdit.text().strip()
        Qty = int(self.lineEdit_4.text().strip())
        Price = int(self.lineEdit_5.text().strip())
        OrgNo = self.lineEdit_6.text().strip()
        ACCNO = self.lineEdit_2.text().strip()
        Order = self.dynamicCall('SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)', ["주식주문", "0107", ACCNO, Type, Code, Qty, Price, HogaGb, OrgNo])
    
    def btn_login(self):
    #         self.excel.addToExcel(self.codelist)
            ret = self.dynamicCall("CommConnect()")
    
    def btn_Quit(self):
        self.dynamicCall("CommTerminate()")
        sys.exit()
    
    def OnEventConnect(self, nErrCode):
        if nErrCode == 0:
            self.textEdit.append("서버에 연결 되었습니다...")
            print("서버에 연결 되었습니다...")
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(True)
            self.SendOrder.setEnabled(True)
            self.textEdit.setEnabled(True)
            self.comboBox.setEnabled(True)
            self.comboBox_2.setEnabled(True)
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setEnabled(False)
            self.lineEdit_5.setEnabled(True)
            self.lineEdit_6.setEnabled(True)
            self.lineEdit_8.setEnabled(True)
            self.lineEdit_9.setEnabled(True)
            self.lineEdit_10.setEnabled(True)
            self.lineEdit_4.setEnabled(True)
    
        else:
            self.textEdit.append("서버 연결에 실패 했습니다...")
            print("서버 연결에 실패 했습니다...")
    
    def OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        if sScrNo == "0003":
            print(sMsg)
            self.textEdit.append(sMsg)
    
        else:
            print(sMsg)
            self.textEdit.append(sMsg)
    
    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList):
        self.lineEdit_6.setText(self.GetChjanData(9203))
        
        self.textEdit.append("주문번호: "+self.GetChjanData(9203))
        self.textEdit.append("종 목 명: "+self.GetChjanData(302))
        self.textEdit.append("주문수량: "+self.GetChjanData(900))
        self.textEdit.append("주문가격: "+self.GetChjanData(901))
