# -*- coding: utf-8 -*-
import ExcelMake
import multiprocessing as mp



class ExcelMakeForProcess:

	def doRead(self,queue):
		q=queue
        
		self.excelMake = ExcelMake.ExcelCode(False)
		self.excelMake.ExcelRead()
		self.excelMake.excelVisible()
        

		codelist = self.excelMake.getCodeList()

		for code in codelist:
			q.put(code)
		q.put('END')

	def doParse(self,readQueue,writeQueue):

		q=readQueue
		wq = writeQueue

		i=0
		# while True:
		while i<10:
			code = q.get()
			if code== 'END':
				wq.put('END')
				break

			timePerDict = self.excelMake.getPercent(code)
			wq.put(timePerDict)
			i+=1
		return wq        

			
	def doWrite(self,writeQueue):

		wq=writeQueue

		print('claal!')

		while True:
			TimePerDict = wq.get()
			if TimePerDict == 'END':
				break;
			print(TimePerDict)




if __name__ == '__main__':
    # tt = ExcelMake.ExcelCode(False)

    exmp= ExcelMakeForProcess()

    
    writeQueue=mp.Queue()
    
    readQueue=mp.Queue()

#     writeQueue.close()
#     readQueue.close()
    
    while writeQueue.empty()==False:
        writeQueue.get()
    
    while readQueue.empty()==False:
        readQueue.get()
    
    exmp.doRead(readQueue)
    writeQueue= exmp.doParse(readQueue,writeQueue)
    exmp.doWrite(writeQueue)
    
    
    
#     exmp.doWrite(queue)

    # tt.ExcelRead()
    # tt.excelVisible()
    # tt.setAllValue()
    # tt.ExcelExitWithSave()
