# -*- coding: utf-8 -*-

import win32com.client
import ExcelMake
import time

class ExcelParser:
    
    def __init__(self):
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.readedExcel = ExcelMake.ExcelCode(False)
        self.readedExcel.ExcelRead()

        self.codelist = self.readedExcel.getCodeList()

        self.wb = self.readedExcel.getWorkBook()
        self.ws = self.readedExcel.getWorkSheet()
        
    def parse(self):

        # for index in range(2,len(self.codelist)+1):
        #     self.MuchVal = 
        #     print(index)
        i=2
        self.value=self.codelist
        try:
            ft_time=time.time()
            print(int(self.ws.Cells(i,1).Value))
            while(int(self.ws.Cells(i,1).Value) != 1000):
                
                start_time=time.time()
                print(str(self.value[int(self.ws.Cells(i,1).Value)])+' parse . . . .')
                j=3
                self.value[int(self.ws.Cells(i,1).Value)]=[]
                while(int(self.ws.Cells(1,j).Value) !=1451):
                    try:
                        self.value[int(self.ws.Cells(i,1).Value)].append(round(self.ws.Cells(i,j).Value*100,2))
#                         print(round(self.ws.Cells(i,j).Value*100,2))
                        j+=1
                    except TypeError:
                        j+=1
                        continue
                print('set ['+str(self.ws.Cells(i,2).Value)+': '+str(i-1)+'/'+str(len(self.value))+']. '+str(time.time()-start_time))

                i+=1
            print('time :'+str(time.time()-ft_time))
        except KeyError:
            print('KeyError end')
        return self.value

    def getValue(self):
    	return self.value

    def getCodelist(self):
    	return self.codelist
        
if __name__ == '__main__':
    test = ExcelParser()
    test.parse()
#     testval = {}
#     
#     testval['hi']=[23]
#     testval['hi'].append(32)
#     
#     print(testval)