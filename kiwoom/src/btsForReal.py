# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import requests
import time

class btsForReal:

	def  UrlParsing(self):

		frame_src = 'http://finance.daum.net/item/main.daum?code=003000'
		self.iframe_content=BeautifulSoup(requests.get(frame_src).text,"lxml")
		
		curPrice = self.iframe_content.findAll("em", class_="curPrice up")
		if len(curPrice) == 0:
			curPrice = self.iframe_content.findAll("em", class_="curPrice down")
		print(curPrice[0].contents[0])

if __name__=="__main__":

	test = btsForReal()

	test.UrlParsing()