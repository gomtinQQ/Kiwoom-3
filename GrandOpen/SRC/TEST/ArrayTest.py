# -*- coding: utf-8 -*-

if __name__ == '__main__':
    
    arr = []
    
    
    StockCode = "23232"
    StockName = "이화공영"
    
    codeSet = StockCode,StockName
    arr.append(codeSet)
    
    StockCode = "11111"
    StockName = "하이비젼"
    codeSet = StockCode,StockName
    arr.append(codeSet)
    
    for i in range(len(arr)):
        print(arr[i][1])
    