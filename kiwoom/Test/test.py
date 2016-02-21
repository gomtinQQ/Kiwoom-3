import requests
import json
import time

class GoogleFinanceAPI:
    def __init__(self):
        self.prefix = "http://finance.google.com/finance/info?client=ig&q="
    
    def get(self,symbol,exchange):
        url = self.prefix+"%s:%s"%(exchange,symbol)
        u = requests.get(url)
        content = u.text
        
        obj = json.loads(content[3:])
        return obj
        
        
if __name__ == "__main__":
    c = GoogleFinanceAPI()
    
    while 1:
        quote = c.get("126700","KOSDAQ")
        print(quote)
        time.sleep(30)