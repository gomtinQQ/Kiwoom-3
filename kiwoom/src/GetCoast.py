# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *
from PyQt4.QtCore import QVariant
import re
import ExcelMake
from bs4 import BeautifulSoup



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

#class Ui_Form(object):
class Ui_Form(QAxWidget):
    def __init__(self):
        super().__init__()
        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')
        self.connect(self, SIGNAL("OnEventConnect(int)"), self.OnEventConnect)
        self.connect(self, SIGNAL("OnReceiveMsg(QString, QString, QString, QString)"), self.OnReceiveMsg)
        self.connect(self, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self.OnReceiveTrData)
        self.connect(self, SIGNAL("OnReceiveChejanData(QString, int, QString)"),self.OnReceiveChejanData)
#         self.ExcelList = list
#         self.excel = ExcelMake.ExcelCode()
        


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
            self.ExtractExcel.setEnabled(True)
            self.Massive.setEnabled(True)
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
        

    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSPlmMsg):

        if sTrCode == "OPT10001":
            
            cnt = self.dynamicCall('GetRepeatCnt(QString, QString)', sTrCode, sRQName)
            ItemName = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "종목명")
            CurrCoast = self.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTrCode, "", sRQName, 0, "현재가")
            
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
                
        if sTrCode == "OPT10071":
            
            print('Called OPT10071')
            cnt = self.dynamicCall('GetRepeatCnt(QString, QString)', sTrCode, sRQName)
            cnt=int(cnt)
            print('########### count ##########'+str(cnt))
            vTemp = self.dynamicCall('GetCommDataEx(QString,QString)',"OPT10071","시간대별전일비거래비중")
            rTemp = self.dynamicCall('GetCommData(QString,QString,int,QString)',"OPT10071","sRQname",0,"시간")
            print('vtemp'+str(vTemp))
            print('rtemp'+str(rTemp))
                    
                
        

    def btn_clicked3(self):
        Code = self.lineEdit.text().strip()
        ret = self.dynamicCall('SetInputValue(QString, QString)', "종목코드", Code)
        ret = self.dynamicCall('CommRqData(QString, QString, int, QString)', "주식기본정보", "OPT10001", 2, "0101")
        print(str(ret)+"코드")
         
    def getTotalInfo(self):    
        ret = self.dynamicCall('SetInputValue(QString, QString)', "업종코드", '101')
        ret = self.dynamicCall('CommRqData(QString, QString, int, QString)', "주식기본정보", "OPT20003", 2, "0102")
        ret = self.dynamicCall('SetInputValue(QString, QString)', "업종코드", '001')
        ret = self.dynamicCall('CommRqData(QString, QString, int, QString)', "주식기본정보", "OPT20003", 2, "0101")
        print(str(ret)+"코드")

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
        print(ACCNO)
        
            
    def btn_ExtractExcel(self):
        self.codelist = self.GetCodeListByMarket(10)
        self.excel = ExcelMake.ExcelCode()          #클릭때마다 객체가생성됨.
        self.excel.addToExcel(self.codelist)
        self.namelist =self.codelist.split(';')
        
        
        for a in self.namelist: #a 종목명
            self.excel.addToExcelCodeName(self.GetMasterCodeName(a)) #종목코드
              
#             rett=self.dynamicCall('SetInputValue(QString,QString)',"종목코드",a)
#             print("rett1 : "+str(rett))
#             rett=self.dynamicCall('SetInputValue(QString,QString)',"시간구분",10)
#             print("rett2 : "+str(rett))
#             rett=self.dynamicCall('CommRqData(QString, QString, int, QString)',"주식기본정보", "OPT10071",2,"0102")
#             print(str(rett)+"코드!")

        self.excel.excelVisible()
        

    def getMassiveData(self):
        print()
        print('==================MassiveData Call======================')
        
        self.codelist = self.GetCodeListByMarket(10)
        self.namelist =self.codelist.split(';')
#         for a in self.namelist:
#             print('a '+str(a))
#             print('codename '+str(self.GetMasterCodeName(a)))
        retInput = self.dynamicCall('SetInputValue(QString,QString)','종목코드','000660')
             
#             print("retInput1"+str(retInput))
        retInput = self.dynamicCall('SetInputValue(QString,QString)','시간구분','10')
        rets= self.dynamicCall('CommRqData(QString,QString,int,QString)','RQName','OPT10071','0','화면번호')
               
              
#             print("retInput2"+str(retInput))
        print("reslt"+str(rets))
        
        print('==================MassiveData End======================')
        
        

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

        
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(700, 450)
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 231, 400))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayoutWidget = QtGui.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 20, 191, 281))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit)
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_4 = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_4)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_5 = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit_5.setEnabled(False)
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.lineEdit_5)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_6 = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit_6.setEnabled(False)
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.lineEdit_6)
        
        self.label_8 = QtGui.QLabel(self.formLayoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_8)
        self.lineEdit_8 = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit_8.setEnabled(False)
        self.lineEdit_8.setObjectName(_fromUtf8("lineEdit_8"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.lineEdit_8)
        
        self.label_9 = QtGui.QLabel(self.formLayoutWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_9)
        self.lineEdit_9 = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit_9.setEnabled(False)
        self.lineEdit_9.setObjectName(_fromUtf8("lineEdit_9"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.lineEdit_9)
        
        self.label_10 = QtGui.QLabel(self.formLayoutWidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.LabelRole, self.label_10)
        self.lineEdit_10 = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit_10.setEnabled(False)
        self.lineEdit_10.setObjectName(_fromUtf8("lineEdit_10"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.lineEdit_10)
        
        self.comboBox = QtGui.QComboBox(self.formLayoutWidget)
        self.comboBox.setEnabled(False)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBox)
        
        self.comboBox_2 = QtGui.QComboBox(self.formLayoutWidget)
        self.comboBox_2.setEnabled(False)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.comboBox_2)
        
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setEnabled(False)
        self.pushButton.setGeometry(QtCore.QRect(120, 330, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.connect(self.pushButton, SIGNAL("clicked()"), self.btn_clicked3)
        
        self.SendOrder = QtGui.QPushButton(self.groupBox)
        self.SendOrder.setEnabled(False)
        self.SendOrder.setGeometry(QtCore.QRect(10, 330, 75, 23))
        self.SendOrder.setObjectName(_fromUtf8("SendOrder"))
        self.connect(self.SendOrder, SIGNAL("clicked()"), self.btn_SendOrder)
        
        self.ExtractExcel = QtGui.QPushButton(self.groupBox)
        self.ExtractExcel.setEnabled(False)
        self.ExtractExcel.setGeometry(QtCore.QRect(10, 360, 75, 23))
        self.ExtractExcel.setObjectName(_fromUtf8("ExtractExcel"))
        self.connect(self.ExtractExcel, SIGNAL("clicked()"), self.btn_ExtractExcel)
        
        self.Massive= QtGui.QPushButton(self.groupBox)
        self.ExtractExcel.setEnabled(False)
        self.Massive.setGeometry(QtCore.QRect(100, 360, 75, 23))
        self.Massive.setObjectName(_fromUtf8("Massive"))
        self.connect(self.Massive, SIGNAL("clicked()"), self.getMassiveData)
        
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setEnabled(False)
        self.textEdit.setGeometry(QtCore.QRect(270, 20, 331, 211))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(390, 250, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.btn_login)
        
        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(480, 250, 75, 23))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.connect(self.pushButton_4, SIGNAL("clicked()"), self.btn_Quit)
        

        
        
        
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 300, 61, 23))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.connect(self.pushButton_3, SIGNAL("clicked()"), self.btn_info)
        
        self.lineEdit_2 = QtGui.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 300, 141, 20))
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))

        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(350, 270, 211, 20))
        self.label_7.setStyleSheet(_fromUtf8("color: rgb(85, 170, 255);"))
        self.label_7.setIndent(-1)
        self.label_7.setOpenExternalLinks(True)
        self.label_7.setObjectName(_fromUtf8("label_7"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "키움 API", None))
        self.groupBox.setTitle(_translate("Form", "주문입력", None))
        self.label.setText(_translate("Form", "종목코드", None))
        self.label_2.setText(_translate("Form", "거래구분", None))
        self.label_3.setText(_translate("Form", "매매구분", None))
        self.label_4.setText(_translate("Form", "주문수량", None))
        self.label_5.setText(_translate("Form", "주문가격", None))
        self.label_6.setText(_translate("Form", "원주문번호", None))
        self.label_8.setText(_translate("Form", "총주식갯수", None))
        self.label_9.setText(_translate("Form", "거래소", None))
        self.label_10.setText(_translate("Form", "코스닥", None))
        self.comboBox.setItemText(0, _translate("Form", "00: 지정가", None))
        self.comboBox.setItemText(1, _translate("Form", "03: 시장가", None))
        self.comboBox.setItemText(2, _translate("Form", "61: 시간외 단일가", None))
        self.comboBox_2.setItemText(0, _translate("Form", "1:   매   수", None))
        self.comboBox_2.setItemText(1, _translate("Form", "2:   매   도", None))
        self.comboBox_2.setItemText(2, _translate("Form", "3:   매수취소", None))
        self.comboBox_2.setItemText(3, _translate("Form", "4:   매도취소", None))
        self.pushButton.setText(_translate("Form", "GetInfo", None))
        self.SendOrder.setText(_translate("Form", "주 문", None))
        self.ExtractExcel.setText(_translate("Form", "액셀로 추출", None))
        self.Massive.setText(_translate("Form", "대량데이타", None))
        self.pushButton_2.setText(_translate("Form", "로그인", None))
        self.pushButton_4.setText(_translate("Form", "종 료", None))
        self.pushButton_3.setText(_translate("Form", "계좌조회", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

