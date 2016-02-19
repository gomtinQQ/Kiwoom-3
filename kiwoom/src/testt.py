from DashinDbMake import DashinDbMake 
import time
import ExcelMake

# dd.createTable()
# proc = mp.Process(target=dd.doWork)
# proc.start()
# proc.join()


def main():

    dd = DashinDbMake()
    
    
    dd.start()

#     while True:
#         if dd.getTimeSource()=='900':
#             break
#         else: 
#             print(dd.getTime())
#             time.sleep(1)
    dd.join()
    
    pro = ExcelMake.ExcelCode(setLayout=False)
    time.sleep(600)
    pro.start()    

    
if __name__== '__main__':
    main()