# -*- coding: utf-8 -*-
import win32com.client
import bts
import time
import os
import shutil

class ExcelCode:
    
    
    def __init__(self,setLayout=True):
        '''엑셀 초기화 '''
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.bt = bts.mbts()
        
        if setLayout==True:
            self.setLayout()
        
    def setLayout(self):
        '''Layout init'''
        
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
        
        
    def addToExcel(self,codelist):
        '''코드리스트를 받으면 각 코드들 세로로 추가'''
        self.codelist=codelist.split(';')
        i=2
        
        start_time=time.time()
        for a in self.codelist:
            self.ws.Cells(i,1).Value = a
            i += 1
        end_time=time.time()
        print('CodeList Added  ['+str(end_time-start_time)+']')
        
        
    def addToExcelCodeName(self,mylist):
        
        self.ws.Cells(self.j,2).Value=mylist
        self.j+=1

    def excelVisible(self):
        self.excel.Visible = True

    
    def addZeroToStockCode(self,str):
        str=str.strip()

        if len(str.strip())<=6:
            while(len(str.strip())!=6):
                str=str[:0]+"0"+str[0:]
        return str
    
    def ExcelRead(self,fileName=''):
        
        if fileName =='':
            fileName = 'D:\\Kiwoo\\ExcelData\\yang_1'
            
        self.wb = self.excel.Workbooks.Open(fileName)
        self.ws = self.wb.ActiveSheet
#         self.dictCodeList=self.getCodeList()
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
            print(str(i-1)+'th setting. . . ['+str(self.ws.Cells(i,2).Value)+']')
            i+=1


        print('IndexCode Value Setting(IndexCode[Index]=StockCode) ['+str(time.time()-start_time)+']')

        return IndexCode

    
    def setPercent(self,code,TimePerDict):
        
#         TimePerDict = self.codeParse(code)
        
        code=int(code)
        i = self.dictCodeList[code]
        j=3
        _start_time = time.time()
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
        print('setting . . '+str(time.time()-_start_time))
    
    
    def codeParse(self,code):
        self.bt.IframeUrlWithCode(self.addZeroToStockCode(str(code)))
        
        return self.bt.getTimePerDic()
        
        
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


    def ExcelExitWithoutSave(self):
        
        self.wb.Close(False)
        self.excel.DisplayAlerts = False
        self.excel.Quit()
        del self.ws
        del self.excel
    
    def ExcelExitWithSave(self):
        
        fileName=self.getFileNameForsave()
        self.wb.SaveAs(fileName)
        
        
        self.ExcelExitWithoutSave()

    
    def setAllValue(self):
        
        start_time=time.time()
        all =2
        self.dictCodeList=self.getCodeList()
        
        while(self.ws.Cells(all,1).Value is not None):
            code = self.ws.Cells(all,1).Value
            name = str(self.ws.Cells(all,2).Value)
            print('======================================================================')
            print('['+name+']setting. . . .')
            self.setPercent(int(code),self.codeParse(int(code)))
            print('['+name+']setting finish ['+str(int(all)-1)+'/'+str(len(self.dictCodeList))+']')
            all+=1
            
        end_time=time.time()
        print('total items ['+str(all)+']'+' time ['+str(end_time-start_time)+']  success!!')
        
        
if __name__ == '__main__':
    tt = ExcelCode(setLayout=False)

    tt.ExcelRead()
    tt.excelVisible()
    tt.setAllValue()
    tt.ExcelExitWithSave()
    
    
