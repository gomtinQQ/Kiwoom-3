# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import requests
import time

import ExcelMake

class btsForReal:

	def  UrlParsing(self,code):

# 		_start=time.time()
		frame_src = 'http://finance.daum.net/item/main.daum?code='+str(code)
		self.iframe_content=BeautifulSoup(requests.get(frame_src).text,"lxml")

		curPrice = self.iframe_content.findAll("em", class_="curPrice up")
		if len(curPrice) == 0:
			curPrice = self.iframe_content.findAll("em", class_="curPrice down")
			if len(curPrice) ==0:
				curPrice = self.iframe_content.findAll("em", class_="curPrice keep")
		print(curPrice[0].contents[0])
# 		print((time.time()-_start))
		
	
	
	def listUrlParse(self,codelist):
		_start=time.time()
		
		
		for code in codelist:
			print(code)
			self.UrlParsing(self.addZeroToStockCode(str(code)))
			
		print((time.time()-_start))
		
	
	def addZeroToStockCode(self,str):
		str=str.strip()

		if len(str.strip())<=6:
			while(len(str.strip())!=6):
				str=str[:0]+"0"+str[0:]
		return str	
	
		
if __name__=="__main__":

	
	tt=ExcelMake.ExcelCode(False)
	tt.ExcelRead()
	tt.excelVisible()
	codelist=tt.getCodeList()
	
	test = btsForReal()
	test.listUrlParse(codelist)