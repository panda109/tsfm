# -*- coding: UTF-8 -*-
'''
Created on Feb 11, 2022

@author: shawn
'''
import sqlite3, requests
import os, logging, time, json
from datetime import datetime, timedelta
from monitor.gen_post import GenPosts
from monitor.find_group_diff import find_group_diff

intMonitorInterval = 300
intTimeZoneHour = 8
intCheckNoPowerInterval = 600
strDB_Test = 'data-test.sqlite'

objLogger = logging.getLogger(__name__)

def monitorPV(strDBPath,strSolarModels):
    objPost = GenPosts('zh_tw') # 2022.02.11 need to load locale setting in the future
    try:
        while True:
            # connect to sqlite3 DB
            objConn = sqlite3.connect(os.path.join(strDBPath,strDB_Test))
            objCursor = objConn.cursor()
            
            objNow = datetime.now()
            """
            # remove old data (24-hours-before)
            objLogger.info('Start to delete old data....')
            objDateTimeToBeDelete = objNow - timedelta(hours=24)
            intTimeStamp_ToBeDelete = int(objDateTimeToBeDelete.timestamp()*1000)
            objLogger.debug('Data before %s would be deleted!' % intTimeStamp_ToBeDelete)
            
            objCursor.execute("delete from device_data where generated_time < %s" % intTimeStamp_ToBeDelete)
            objConn.commit()
            objLogger.info('Finish deleting....')
            objCursor.execute("vacuum")
            objLogger.info('Run vacuum to reduce DB size....')
            time.sleep(5)
            """
            # start to query and notify           
            objCursor = objConn.execute("select * from device_info where model in %s and notify = 'ON'" % strSolarModels)
            listResults = objCursor.fetchall()
            #objLogger.debug('listResults: %s' % str(listResults))
            for listDevice in listResults:
                objLogger.debug('listDevice: %s' % str(listDevice))
                objNewDateTime = objNow + timedelta(hours=intTimeZoneHour)
                #objNewDateTime = objNow # for testing in my mac
                intCurrentHour = int(objNewDateTime.strftime("%H"))
                objLogger.info('Current hour: %s' % intCurrentHour)
                
                if intCurrentHour >= listDevice[9] and intCurrentHour <= listDevice[10]: # Time period to check power
                    intTimeStamp_Now = int(objNow.timestamp()*1000)
                    strFrom = objNow.strftime("%Y-%m-%d 00:00:00")
                    objFrom = datetime.strptime(strFrom,"%Y-%m-%d %H:%M:%S")
                    intTimeStamp_Start = int(objFrom.timestamp()*1000)
                    strNowTime = objNow.strftime("%H:%M")

                    strSQL = """select value,generated_time from device_data where 
                    model in %s and scope = 'generatedElectricity' and dev_uuid = '%s' and 
                    generated_time >= %s and generated_time <= %s 
                    order by generated_time desc
                    """
                    objCursor = objConn.execute(strSQL % (strSolarModels,listDevice[0],intTimeStamp_Start,intTimeStamp_Now))
                    listResults = objCursor.fetchall()
                    if listResults != []:
                        if listResults[0][0] is not None:
                            objLogger.debug('litResults[0]: %s' % listResults[0])
                            objLogger.debug('litResults[-1]: %s' % listResults[-1])
                            
                            if intTimeStamp_Now - listResults[0][1] >= intCheckNoPowerInterval * 1000: 
                                # NoPowerGeneration for more than 10 minutes (60 * 10 * 1000)
                                objLogger.debug('call NoPowerGeneration post...')
                                
                                dicPost = objPost.NoPowerGeneration(listDevice[1],str(intCheckNoPowerInterval/60))
                                objResponse = requests.post(objPost.strURL_ServiceStore + objPost.strPath_Post % listDevice[5], 
                                                            data = json.dumps(dicPost), 
                                                            headers = objPost.dicHeader)
                                objLogger.debug('Send notify: %s, %s' % (objResponse,objResponse.content))
                                objLogger.debug('')
                                
                            elif (listResults[0][0] - listResults[-1][0]) * 1000 < listDevice[7] * 1000 * (listDevice[8]/100):
                                # LowPowerGeneration
                                objLogger.debug('call LowPowerGeneration post...')
                                
                                # strPVName, strStartTime, strEndTime, intTotal, intTargetTotal, intTargetPercent
                                dicPost = objPost.LowPowerGeneration(listDevice[1],'00:00',strNowTime,
                                                                     listResults[0][0],listDevice[7],listDevice[8])
                                objResponse = requests.post(objPost.strURL_ServiceStore + objPost.strPath_Post % listDevice[5], 
                                                            data = json.dumps(dicPost), 
                                                            headers = objPost.dicHeader)
                                objLogger.debug('Send notify: %s, %s' % (objResponse,objResponse.content))
                                
                                objLogger.debug('')
            
            find_group_diff('sqlite',objConn,strSolarModels,objPost,str(intCheckNoPowerInterval/60))
            
            objConn.close()
            time.sleep(intMonitorInterval)
            
    except Exception as error:
        objLogger.error(error, exc_info=True)


if __name__ == '__main__':
    pass
    
