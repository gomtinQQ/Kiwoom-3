# -*- coding: utf-8 -*-

import btsForDashin
import DBMake
import sys
import time
from _sqlite3 import OperationalError

if __name__=="__main__":
    
#     str="09:1"
#     
#     if str.index(":")>0:
#         
#         print("True")
#         str=str[:str.index(":")]+str[str.index(":")+1:]
#     if len(str)<4:
#         str=str[:2]+'0'+str[2:]
#         print(len(str))
#     print(str)

    now = time.localtime()
    Hour = now.tm_hour
    Minute=now.tm_min
    print(str(Hour) +':'+ str(Minute))
    
    dbm = DBMake.dbm2()
    bfd = btsForDashin.btsForReal()
    bfd.UrlParsing()
    codeNameCoast = bfd.getCodeNameCoast()
    
            
    try:
        dbm.createTable("D:\\OneDrive\\python\\sqlite3\\kosdaqDashin_0210.db")
    except OperationalError :
           
        print(str(sys.exc_info()))
           
    for code in codeNameCoast:
        for name in codeNameCoast[code]:
#             dbm.setCode(code,name)
            dbm.updateCode(code,'9:52',codeNameCoast[code][name])

    

    
    dbm.commit()