#coding=cp936
import random
import logging

def int2hex(number, length):
    s = hex(number)[2:]
    
    return "0"*(length-len(s))+s

def GenTranID():
    a =''
    for i in xrange(32):
        a+=random.choice('0123456789ABCDEF')
    #return binascii.a2b_hex(a)
    return a

class logger:
    def __init__(self, logFile):
        self.logger = logging.getLogger()
            
        hdlr = logging.FileHandler(logFile)
        formatter = logging.Formatter('%(asctime)s--%(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.NOTSET)
        
    def log(self, msg, level):
        #msg:the log message
        #level: the log level of the message
        defaultLevel = logging.CRITICAL
        
        LogLevelDict = {logging.CRITICAL:"critical",
                        logging.DEBUG   :"debug"   ,
                        logging.ERROR   :"error"   ,
                        logging.INFO    :"info"    ,
                        logging.WARN    :"warn"    }
                            
        if not (level > defaultLevel):
            print msg
            fun = getattr(self.logger, LogLevelDict[level])
            fun(msg)
        else:
            pass
        
   
"""     
def initLogger(logFile):
    
    
    logger = logging.getLogger()
    
    hdlr = logging.FileHandler(logFile)
    formatter = logging.Formatter('%(asctime)s--%(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    
    return logger

    
def log(msg, level):
    #msg:the log message
    #level: the log level of the message
    logger = initLogger("stun.log")
    defaultLevel = logging.CRITICAL
    
    LogLevelDict = {logging.CRITICAL:"critical",
                    logging.DEBUG   :"debug"   ,
                    logging.ERROR   :"error"   ,
                    logging.INFO    :"info"    ,
                    logging.WARN    :"warn"    }
                    
    if not (level > defaultLevel):
        print msg
        fun = getattr(logger, LogLevelDict[level])
        fun(msg)
    else:
        pass
"""

if __name__ == "__main__":
    """
    logger = initLogger("test.log")
    logger.debug("debug ")
    logger.info("info")
    getattr(logger, "warn")("warn")
    """
    log = logger("stun.txt")
    log.log("debug", logging.DEBUG)
    log.log("warn", logging.WARN)
    log.log("info", logging.INFO)