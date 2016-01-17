# -*- coding: utf-8 -*-

import win32com.client

import bts
import time
import os
import shutil

class ExcelCode:
    
    
#     엑셀 초기화 및 시간설정
    def __init__(self,setLayout=True):
        self.excel = win32com.client.Dispatch("Excel.Application")

        if setLayout==True:
            self.setLayout()
        
    def setLayout(self):
        self.wb = self.excel.Workbooks.Add()
        self.ws = self.wb.Worksheets("Sheet1")
        self.ws.Cells(1,1).Value ="StockCode"
        self.ws.Cells(1,2).Value ="StockName"
        self.j=2
        print('Excel Object Created')
        
        print('Making Excel..')        
        totalMinute=3
        for i in range(9,15):##시간 분단위로 설정.
            for j in range(0,60):
                if j<10:
                    j=str(j)
                    j=j[:0]+str('0')+j[0:]
                self.ws.Cells(1,totalMinute).Value =str(i)+str(j)
                totalMinute+=1
                
        print('excel init end')
        
        
#     코드리스트를 받으면 각 코드들 세로로 추가
    def addToExcel(self,codelist):
        self.codelist=codelist.split(';')
        i=2
        
        start_time=time.time()
        for a in self.codelist:
            self.ws.Cells(i,1).Value = a
            i += 1
        end_time=time.time()
        print('CodeList Added  ['+str(end_time-start_time)+']')
#                 코드를받으면 이름으로 추가
#         self.WriteTimePerDict()
    def addToExcelCodeName(self,mylist):
        
        self.ws.Cells(self.j,2).Value=mylist
        self.j+=1

        
    def WritePercentage(self):

        start_time=time.time()
        bt = bts.mbts()
        code='000660'
        bt.IframeUrlWithCode(code)
        codeCurrList = bt.getEachPercent()
        
        c =3
        d =2
        
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
        
    # def getCodeList(self):
    #     return self.codelist
    
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
        try:
            self.wb = self.excel.Workbooks.Open(fileName)
        except Exception:
            filePath = 'D:\\Kiwoo\\ExcelData'
            now = time.localtime()
            nowYear =now.tm_year
            nowMon =now.tm_mon
            nowmDay = now.tm_mday
            nowmDay=int(nowmDay)-1
            if nowmDay<1:
                nowMon = int(nowMon)-1
                if nowMon<1:
                    nowYear = int(nowYear)-1
            if int(nowMon) <10:
                nowMon=str(nowMon)
                nowMon=nowMon[:0]+'0'+nowMon[0:]
            if int(nowmDay) <10:
                nowmDay=str(nowmDay)
                nowmDay=nowmDay[:0]+'0'+nowmDay[0:]
            dirPath= filePath+str('\\')+str(nowYear)+str(nowMon)+str(nowmDay)
            
            if not os.path.isdir(dirPath):
                os.mkdir(dirPath)
            self.logCount=1
            fileName = dirPath+str('\\')+str(nowYear)+str(nowMon)+str(nowmDay)+str('_yang_')+str(self.logCount)+str('.xlsx')
            shutil.copy(fileName,self.getFileName())
            self.wb = self.excel.Workbooks.Open(fileName)
        
        self.ws = self.wb.ActiveSheet
        
        # self.dictCodeList=self.setCodeList();
        print('read success')

    def getWorkBook(self):
        return self.wb

    def getWorkSheet(self):
        return self.ws
        
    def getCodeList(self):
        i=2
        codelistforIndex ={}
        start_time = time.time()
        while(self.ws.Cells(i,1).Value is not None):
            codelistforIndex[int(self.ws.Cells(i,1).Value)]=i
            i+=1
        
        print('codelistforIndex value setting (codelistforIndex[StockCode]=Index) ['+str(time.time()-start_time)+']')
        return codelistforIndex
    
    def getIndexCode(self):

        i=2
        IndexCode={}
        start_time = time.time()

        while(self.ws.Cells(i,1).Value is not None):
            IndexCode[i]=int(self.ws.Cells(i,1).Value)
            i+=1


        print('IndexCode Value Setting(IndexCode[Index]=StockCode) ['+str(time.time()-start_time)+']')

        return IndexCode


    # def getTimePetDict(self,code):
    #     bt = bts.mbts()
        
    #     bt.IframeUrlWithCode(code)
    #     TimePerDict = bt.getTimePerDic()
            
    #     i=2
    #     j=3

    #     while(self.ws.Cells(i,1).Value is not None):
    #         print(int(self.ws.Cells(i,1).Value))

    #         print(int(code))
            
    #         if int(code) == int(self.ws.Cells(i,1).Value):
    #             while(int(self.ws.Cells(1,j).Value) != 1451):
    #                 try:
    #                     timeVal= str(int(self.ws.Cells(1,j).Value))
    #                     if int(timeVal[:1])==9:
    #                         timeVal=timeVal[:0]+str('0')+timeVal[0:]
    #                     timeVal= timeVal[:2]+str(':')+timeVal[2:]
    #                     self.ws.Cells(i,j).Value=TimePerDict[timeVal]
    #                     j+=1
    #                 except KeyError:
    #                     j+=1
    #                     continue
    #         j=3
    #         i+=1
    #     print('성공!')
    
    def setPercent(self,code):
        bt = bts.mbts()
        code=self.addZeroToStockCode(str(code))
        bt.IframeUrlWithCode(code)
        
        
        code=int(code)
        i = self.dictCodeList[code]
        
        TimePerDict = bt.getTimePerDic()
        
        j=3
        while(int(self.ws.Cells(1,j).Value != 1451)):
            try:
                timeVal= str(int(self.ws.Cells(1,j).Value))
                if int(timeVal[:1])==9:
                    timeVal=timeVal[:0]+str('0')+timeVal[0:]
                timeVal= timeVal[:2]+str(':')+timeVal[2:]
                self.ws.Cells(i,j).Value=TimePerDict[timeVal]
                j+=1 
            except KeyError:
                j+=1
                continue
        
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
        self.excel.DisplayAlerts = False
        self.excel.Quit()
        del self.ws
        del self.excel
    
    def ExcelExitWithSave(self):
        
        self.saveas()
        
        self.wb.Close(False)
        self.excel.DisplayAlerts = False
        self.excel.Quit()
        del self.ws
        del self.excel
    
    def setAllValue(self):
        
        start_time=time.time()
        all =2
        self.dictCodeList=self.getCodeList()
        while(self.ws.Cells(all,1).Value is not None):
            print('======================================================================')
            print('['+str(self.ws.Cells(all,2).Value)+']setting. . . .')
            self.setPercent(int(self.ws.Cells(all,1).Value))
            print('['+str(self.ws.Cells(all,2).Value)+']setting finish ')
            all+=1
            
        end_time=time.time()
        print('total items ['+str(all)+']'+' time ['+str(end_time-start_time)+']  success!!')
        
if __name__ == '__main__':
    tt = ExcelCode(False)
    
#     tt.ExcelExitWithSave()

    tt.ExcelRead()
    tt.excelVisible()
    tt.setAllValue()
#     tt.setPercent('003800')
#     tt.setPercent('900080')
#     
#     tt.setPercent('900110')
#     
#     tt.setPercent('900130')
#     
#     tt.setPercent('900180')
#     tt.setPercent('000250')
    
    
    
