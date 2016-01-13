# -*- coding: utf-8 -*-

import win32com.client

import bts
import time
import os

class ExcelCode:
    
    
#     엑셀 초기화 및 시간설정
    def __init__(self):
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.wb = self.excel.Workbooks.Add()
        self.ws = self.wb.Worksheets("Sheet1")
        self.ws.Cells(1,1).Value ="종목코드"
        self.ws.Cells(1,2).Value ="종목명"
        self.j=2
        print('Excel Object Created')
        
        print('Making Excel..')        
        totalMinute=3
        for i in range(9,15):##시간 분단위로 설정.
            for j in range(0,60):
#                 self.ws.Cells(1,totalMinute).Value =str(i)+":"+str(j)
                if j<10:
                    j=str(j)
                    j=j[:0]+str('0')+j[0:]
                self.ws.Cells(1,totalMinute).Value =str(i)+str(j)
                totalMinute+=1
                
#         print(self.ws.Cells(1,1).Value)
#         self.excelVisible()
        
#     코드리스트를 받으면 각 코드들 세로로 추가
    def addToExcel(self,codelist):
        self.codelist=codelist.split(';')
        i=2
        
        start_time=time.time()
        for a in self.codelist:
            self.ws.Cells(i,1).Value = a
            i += 1
        end_time=time.time()
        print('코드리스트 추가  ('+str(end_time-start_time)+')')
#                 코드를받으면 이름으로 추가
        self.WriteTimePerDict()
    def addToExcelCodeName(self,mylist):
        
        self.ws.Cells(self.j,2).Value=mylist
        self.j+=1

        


#####################################################################################
    def WritePercentage(self):

        start_time=time.time()
        bt = bts.mbts()
        code='000660'
        bt.IframeUrlWithCode(code)
        codeCurrList = bt.getEachPercent()
        
        c =3
        d =2
        self.excelVisible()
        for howmanytimes in range(3,self.codelist.__len__()):
            for a in codeCurrList:
                self.ws.Cells(d,c).Value = a
                c+=1
            
            print(str(d-1)+'라인 퍼센테이지 입력 ('+str(time.time()-start_time)+')')
            print('d : '+str(d)+' c : '+str(c)) 
            c =3 #한종목 파싱 다 하면 다시초기화
            d+=1
        print('1100라인  making '+str(time.time()-start_time))
        
    def WriteTimePerDict(self):
        start_time=time.time()
        bt = bts.mbts()
#         self.excelVisible()
        
        for StckCode in self.codelist:
            bt.IframeUrlWithCode(StckCode)
            TimerPerDict = bt.getTimePerDic()
            
            i=1
            while(self.ws.Cells(i,1).Value != None):
                if StckCode == self.ws.Cells(i,1).Value:
                    print('성공') 
                    self.ws.Cells(i,3).Value = 33
                i+=1

    def excelVisible(self):
        self.excel.Visible = True
        
    def getCodeList(self):
        return self.codelist
    
    def saveas(self):

        fileName=self.getFileNameForsave()

        self.wb.SaveAs(fileName)
        self.excel.Quit()
            
    
    def addZeroToStockCode(self,str):
        str=str.strip()

        if len(str.strip())<=6:
            while(len(str.strip())!=6):
                str=str[:0]+"0"+str[0:]
        return str
    
    def ExcelRead(self):
        

        
        fileName = self.getFileName()
        
        self.wb = self.excel.Workbooks.Open(fileName)
        self.ws = self.wb.ActiveSheet
        print('read success')
        
#         print(str(self.ws.Cells(53,2).Value))
        
    def getTimePetDict(self,code):
        bt = bts.mbts()
        
        bt.IframeUrlWithCode(code)
        TimePerDict = bt.getTimePerDic()
            
        i=2
        j=3
#         print(str(self.ws.Cells(i,1).Value))
        while(True):
            print(int(self.ws.Cells(i,1).Value))
            print('hihi')
            print(int(code))
            if int(code) == int(self.ws.Cells(i,1).Value):
                print('나올까 ? ')
                for a in TimePerDict:
                    print('나왔다 !')
                    print(self.ws.Cells(1,j).Value)
                    if self.ws.Cells(1,j).Value == a:
                        self.ws.Cells(i,j).Value = TimerPerDict[a]
                        print(TimePerDict[a])
                    j+=1
            print('한줄완성')
            i+=1
        
        self.excelVisible()
        
        
    def getFileNameForsave(self):
        
        filePath = 'D:\\Kiwoo\\ExcelData'
        now = time.localtime()
        nowYear =now.tm_year
        nowMon =now.tm_mon
        
        
        if int(nowMon) <10:
            nowMon=str(nowMon)
            nowMon=nowMon[:0]+'0'+nowMon[0:]
        nowmDay = now.tm_mday
        if int(nowmDay) <10:
            nowmDay=str(nowmDay)
            nowmDay=nowmDay[:0]+'0'+nowmDay[0:]
        dirPath= filePath+str('\\')+str(nowYear)+str(nowMon)+str(nowmDay)
        
        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)
        self.logCount=1
        
        while(os.path.exists(dirPath+str('\\')+str(nowYear)+str(nowMon)+str(nowmDay)+str('_yang_')+str(self.logCount)+str('.xlsx'))):
            self.logCount+=1
            
        fileName = dirPath+str('\\')+str(nowYear)+str(nowMon)+str(nowmDay)+str('_yang_')+str(self.logCount)+str('.xlsx')
        print('엑셀 추가['+str(fileName)+']')
        return fileName
    
    def getFileName(self):
        
        filePath = 'D:\\Kiwoo\\ExcelData'
        now = time.localtime()
        nowYear =now.tm_year
        nowMon =now.tm_mon
        
        
        if int(nowMon) <10:
            nowMon=str(nowMon)
            nowMon=nowMon[:0]+'0'+nowMon[0:]
        nowmDay = now.tm_mday
        if int(nowmDay) <10:
            nowmDay=str(nowmDay)
            nowmDay=nowmDay[:0]+'0'+nowmDay[0:]
        dirPath= filePath+str('\\')+str(nowYear)+str(nowMon)+str(nowmDay)
        
        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)
        self.logCount=1
        
            
        fileName = dirPath+str('\\')+str(nowYear)+str(nowMon)+str(nowmDay)+str('_yang_')+str(self.logCount)+str('.xlsx')
        print(fileName)
        return fileName
    
    def ExcelExitWithoutSave(self):
        
        self.wb.Close(False)
        self.excel.DisplayAlerts = False        #창보이는걸 방지.
        self.excel.Quit()
        del self.ws
        del self.excel
    
    def ExcelExitWithSave(self):
        
        self.saveas()
        self.excel.Quit()
    
if __name__ == '__main__':
    tt = ExcelCode()
    

    tt.ExcelRead()
    tt.excelVisible()
    tt.getTimePetDict('069110')
#     tt.ExcelExitWithoutSave()
    
