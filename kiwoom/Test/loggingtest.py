import logging
import configparser

import loggingtest2
from logging.handlers import RotatingFileHandler

if __name__ == '__main__':
    
    config = configparser.ConfigParser()
    config.read("../src/config/config.ini")
    print(config.get("DATABASE","VolumeAndForeignAndCompanyDB"))
    
    fName = config.get("LOG","filename")
    lLevel = config.get("LOG","loglevel")
    print(fName,lLevel)
    
    fileHandler = logging.FileHandler("./YGLog.log")
    fileHandler = RotatingFileHandler(filename="./YGLog.log",maxBytes=int(10)*1024*1024)
    
    fomatter = logging.Formatter("[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s")
    fileHandler.setFormatter(fomatter)
    
#     logging.basicConfig(filename="./YGLog.log",level = logging.DEBUG)
    
    logger = logging.getLogger(__name__)
    logger.addHandler(fileHandler)
    logger.setLevel(lLevel)
    
    logger.info("hi")
    logger.warning("hhh")
    logger.debug("uu")
    
    loggingtest2.Bar(logger)
    