import logging
import configparser




class Bar():
    def __init__(self,logger=None):
        self.logger =logger or logging.getLogger(__name__)
        self.logger.debug("from Bar..")


if __name__ == '__main__':
    
#     config = configparser.ConfigParser()
#     config.read("../src/config/config.ini")
#     print(config.get("DATABASE","VolumeAndForeignAndCompanyDB"))
#     
#     fName = config.get("LOG","filename")
#     lLevel = config.get("LOG","loglevel")
#     print(fName,lLevel)
#     
    
    logging.basicConfig(filename="./YGLog.log",level = logging.DEBUG)
    
    logger = logging.getLogger(__name__)
    
    logger.info("hi")
    logger.warning("hhh")
    logger.debug("uu")