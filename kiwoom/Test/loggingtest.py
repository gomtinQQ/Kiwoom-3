import logging
import configparser




if __name__ == '__main__':
    
    config = configparser.ConfigParser()
    config.read("../src/config/config.ini")
    print(config.get("DATABASE","VolumeAndForeignAndCompanyDB"))
    
    fName = config.get("LOG","filename")
    lLevel = config.get("LOG","loglevel")
    print(fName,lLevel)
    
    
    logging.basicConfig(filename="./YGLog.log",level = logging.DEBUG)
    
    logger = logging.getLogger("YGLogger")
    
    logger.info("hi")
    logger.warning("hhh")
    logger.debug("uu")