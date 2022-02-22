# -*- coding: UTF-8 -*-
'''
Created on Feb 10, 2022

@author: shawn
'''
import os, logging, json, time
from datetime import datetime, timedelta
from monitor import NDLogger
from monitor import NDDB
from pathlib import Path

from config import basedir

intMonitorInterval = 300
intWatchInterval = 10
strInverterModelFile = 'inverter_model.json'


def get_inverter_model():
    with open(os.path.join(strCurrentPath,strInverterModelFile)) as fileJson:
        dicData = json.load(fileJson)
    return dicData['model']


if __name__ == '__main__':
    
    # init debug log
    strCurrentPath = os.path.dirname(os.path.realpath(__file__))
    objCurrentPath = Path(strCurrentPath)
    objParentPath = Path(objCurrentPath.parent)
    strTargetLogDir = os.path.join(objParentPath.parent.absolute(),'notify_log')
    
    if not os.path.isdir(strTargetLogDir):
        os.mkdir(strTargetLogDir)
    strLogFile = datetime.now().strftime("TSFM_Notify_%Y%m%d_%H%M%S")
    NDLogger.Logger(strLogFile,strTargetLogDir)
    objLogger = logging.getLogger('tsfm_notify_monitor2')
    objLogger.info('TSFM Notify Monitor starts....')
    

    # check system setting
    strEnv = os.getenv('FLASK_CONFIG')
    # load supported solar inverter model
    listModels = get_inverter_model()
    tupModels = tuple(listModels)
    if len(tupModels) == 1:
        strModle_Tuple = str(tupModels).replace(',','')
    else:
        strModle_Tuple = str(tupModels)
    objLogger.info('Supported models of PV inventer: %s' % strModle_Tuple)

    # for testing
    strEnv = 'testing'
    basedir = objCurrentPath.parent
    #####################
    
    if strEnv == 'production': # load postgresql DB
        from monitor.monitorPo import monitorPo
        
        try:
            thdMonitor = monitorPo(intMonitorInterval,strModle_Tuple)
            thdMonitor.start()
            time.sleep(1)
            while True:
                #break
                #objLogger.info('monitor thread heartbeat...')
                if not thdMonitor.is_alive():
                    objLogger.debug('Original monitor thread is dead. Now re-launch it.')
                    thdMonitor = monitorPo(intMonitorInterval,strModle_Tuple)
                    thdMonitor.start()
                    time.sleep(1)
                    objLogger.info('Re-launch monitor thread id:',thdMonitor.get_thread_ID())
                time.sleep(intWatchInterval)
                
        except Exception as error:
            objLogger.error('Main gets error:',error)

        
    else: # load sqlite DB
        from monitor.monitor_with_sqlite import monitorPV
        import threading
        
        thdNotify = threading.Thread(target = monitorPV, args = (basedir,strModle_Tuple))
        thdNotify.start()
        time.sleep(1)
        while True:
            ##break
            ##objLogger.info('monitor thread heartbeat...')
            if not thdNotify.is_alive():
                objLogger.debug('Original monitor thread is dead. Now re-launch it.')
                thdNotify = threading.Thread(target = monitorPV, args = (basedir,strModle_Tuple))
                thdNotify.start()
                time.sleep(1)
                objLogger.info('Re-launch monitor thread id:',thdNotify.get_thread_ID())
            time.sleep(intWatchInterval)

        
    objLogger.info('Notify monitor is down....')