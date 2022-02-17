#-*- coding: UTF-8 -*-
'''
Created on Jan 17, 2022

@author: shawn
'''
import os, logging.handlers


def Logger(strDebugFile, strOutputFolder):

    objRootLogger = logging.getLogger()
    
    bolDebug = True
    bolConsoleMsg = False
    bolFileMsg = True
    # Debug log levels: DEBUG,INFO,WARNING,ERROR,CRITICAL
    DebugLevel = 'DEBUG'
    strLogFormat = "%(asctime)s - %(process)d:%(thread)d - [%(levelname)s][%(name)s] %(message)s"    

    if not bolDebug:
        objRootLogger.disabled = True
    else:            
        if DebugLevel == 'DEBUG':
            objRootLogger.setLevel(logging.DEBUG)
        elif DebugLevel == 'INFO':
            objRootLogger.setLevel(logging.INFO)
        elif DebugLevel == 'WARNING':
            objRootLogger.setLevel(logging.WARNING)
        elif DebugLevel == 'ERROR':
            objRootLogger.setLevel(logging.ERROR)
        elif DebugLevel == 'CRITICAL':
            objRootLogger.setLevel(logging.CRITICAL)
        
        if bolConsoleMsg:
            # log for console
            strFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            formatter=logging.Formatter(strFormat)
            console=logging.StreamHandler()
            console.setFormatter(formatter)
            objRootLogger.addHandler(console)
        
        if bolFileMsg:
            # log for documentation creation
            strFormat = strLogFormat
            formatter=logging.Formatter(strFormat)
            logfile=os.path.join(strOutputFolder,'%s.log' % strDebugFile)
            #objLogFile=logging.FileHandler(logfile,mode='a')
            objLogFile = logging.handlers.RotatingFileHandler(logfile,mode='a',maxBytes=10485760,backupCount=20,encoding='utf8')
            objLogFile.setFormatter(formatter)
            objRootLogger.addHandler(objLogFile)


if __name__ == '__main__':
    pass