from DashinDbMake import DashinDbMake 
import time
import ExcelMake




def main():

    dd = DashinDbMake()
     
     
 
#     while True:
#         if dd.getTimeSource()>='900' and dd.getTimeSource()<='1500':
    dd.start()
#             break
#         else: 
#             print(dd.getTime())
#             time.sleep(1)
    dd.join()
    

    pro = ExcelMake.ExcelCode()
    
 
    time.sleep(600)
    pro.start()    

    
if __name__== '__main__':
    main()