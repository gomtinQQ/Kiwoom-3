# -*- coding: utf-8 -*-

import win32com.client
from time import sleep
import bts
import time

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
        for i in range(9,15):
            for j in range(0,60):
                self.ws.Cells(1,totalMinute).Value =str(i)+":"+str(j)
                totalMinute+=1
        
        
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
        for b in range(3,1100):
            for a in codeCurrList:
                self.ws.Cells(d,c).Value = a
                c+=1
            print(str(d-1)+'라인 퍼센테이지 입력 ('+str(time.time()-start_time)+')') 
            d+=1
        print('1100라인  making '+str(time.time()-start_time))
        
    def excelVisible(self):
        self.excel.Visible = True
        
    def getCodeList(self):
        return self.codelist
    
    
    def addZero(self,str):
        str=str.strip()

        if len(str.strip())<=6:
            while(len(str.strip())!=6):
                str=str[:0]+"0"+str[0:]
        return str
    
