# -*- coding: UTF-8 -*-
'''
Created on Feb 17, 2022

@author: shawn
'''
import threading,logging,time,requests,json
from datetime import datetime, timedelta
from monitor import NDDB
from monitor.gen_post import GenPosts
from monitor.find_group_diff import find_group_diff
from monitor.update_period_data import update_period_data

intTimeZoneHour = 8
intCheckNoPowerInterval = 600
dicTSFM_DB = {
    'strHost':'pgbouncer-qa.nextdrive.io',
    'strPort':'15432',
    'strUser':'qa_user',
    'strPW':'kGm:A.=#=])6P^6j',
    'strDB':'tsfm'
    }

objLogger = logging.getLogger(__name__)

class monitorPo(threading.Thread):
    def __init__(self,intInterval,strTup_Modle):
        objLogger.debug('Init Monitor class...')
        threading.Thread.__init__(self)
        self.daemon = True
        self.intCheckInterval = intInterval
        self.strSolarModels = strTup_Modle
        self.objPost = GenPosts('zh_tw') # 2022.02.19 need to load locale setting in the future
        intCheckNoPowerInterval = intInterval
    
    
    def get_thread_ID(self):
        return self.strThreadID
    
    def _conn_postgres_db(self):
        self.objTSFMDB = NDDB.NDDB(
                dicTSFM_DB['strHost'],
                dicTSFM_DB['strPort'],
                dicTSFM_DB['strUser'],
                dicTSFM_DB['strPW'],
                dicTSFM_DB['strDB']
                )
        
        self.strSQL_DelData = "Delete from device_data where generated_time < '%s'"
        self.strSQL_FindUser_ON = "select * from public.device_info where model in %s and notify = 'ON'"
        self.strSQL_QueryValue = """select value,generated_time from public.device_data where 
        model in %s and scope = 'generatedElectricity' and dev_uuid = '%s' and 
        generated_time >= %s and generated_time <= %s 
        order by generated_time desc
        """
    
    def run(self):
        self.strThreadID = threading.get_ident()
        try:
            while True:
                self._conn_postgres_db()
                objNow = datetime.now()
                
                update_period_data('postgresql',self.objTSFMDB,self.strSolarModels,intTimeZoneHour)
                
                # remove old data (24-hours-before)
                objLogger.info('Start to delete old data....')
                objDateTimeToBeDelete = objNow - timedelta(hours=24)
                intTimeStamp_ToBeDelete = int(objDateTimeToBeDelete.timestamp()*1000)
                objLogger.debug('Data before %s would be deleted!' % intTimeStamp_ToBeDelete)
                self.objTSFMDB.delete(self.strSQL_DelData % intTimeStamp_ToBeDelete)
                time.sleep(5)
                
                # find users and devices that notify = ON
                listResults = self.objTSFMDB.query(self.strSQL_FindUser_ON % self.strSolarModels)
                #objLogger.debug('find ON user: %s' % str(stResults))
                # uuid,name,model,online_status,gw_uuid,user_id,associated,target_energy_level,lower_bound,start_time,end_time,notify
                for listDevice in listResults:
                    objLogger.debug('listDevice: %s' % str(listDevice))
                    objNewDateTime = objNow + timedelta(hours=intTimeZoneHour)
                    intCurrentHour = int(objNewDateTime.strftime("%H"))
                    objLogger.info('Current hour: %s' % intCurrentHour)
                    
                    if intCurrentHour >= listDevice[9] and intCurrentHour <= listDevice[10]: # Time period to check power
                        intTimeStamp_Now = int(objNow.timestamp()*1000)
                        strFrom = objNow.strftime("%Y-%m-%d 00:00:00")
                        objFrom = datetime.strptime(strFrom,"%Y-%m-%d %H:%M:%S")
                        intTimeStamp_Start = int(objFrom.timestamp()*1000)
                        strNowTime = objNow.strftime("%H:%M")
                        
                        litResults = self.objTSFMDB.query(self.strSQL_QueryValue % (self.strSolarModels,listDevice[0],intTimeStamp_Start,intTimeStamp_Now))
                        #objLogger.debug('litResults: %s' % str(litResults))
                        if litResults != []:
                            if litResults[0][0] is not None:
                                objLogger.debug('litResults[0][0]: %s' % litResults[0][0])
                                objLogger.debug('litResults[-1][0]: %s' % litResults[-1][0])
                                
                                if intTimeStamp_Now - listResults[0][1] >= intCheckNoPowerInterval * 1000: 
                                    # NoPowerGeneration for more than 10 minutes (60 * 10 * 1000)
                                    objLogger.debug('call NoPowerGeneration post...')
                                    
                                    dicPost = self.objPost.NoPowerGeneration(listDevice[1],str(intCheckNoPowerInterval/60))
                                    objResponse = requests.post(self.objPost.strURL_ServiceStore + self.objPost.strPath_Post % listDevice[5], 
                                                                data = json.dumps(dicPost), 
                                                                headers = self.objPost.dicHeader)
                                    objLogger.debug('Send notify: %s, %s' % (objResponse,objResponse.content))
                                    objLogger.debug('')
                                
                                elif (litResults[0][0] - litResults[-1][0])  * 1000 < listDevice[7] * 1000 * (listDevice[8]/100):
                                    # LowPowerGeneration
                                    objLogger.debug('call LowPowerGeneration post...')
                                    
                                    # strPVName, strStartTime, strEndTime, intTotal, intTargetTotal, intTargetPercent
                                    dicPost = self.objPost.LowPowerGeneration(listDevice[1],'00:00',strNowTime,
                                                                              listResults[0][0],listDevice[7],listDevice[8])
                                    objResponse = requests.post(self.objPost.strURL_ServiceStore + self.objPost.strPath_Post % listDevice[5], 
                                                                data = json.dumps(dicPost), 
                                                                headers = self.objPost.dicHeader)
                                    objLogger.debug('Send notify: %s, %s' % (objResponse,objResponse.content))
                                    
                                    objLogger.debug('')
                
                find_group_diff('postgresql',self.objTSFMDB,self.strSolarModels,self.objPost,str(intCheckNoPowerInterval/60))
                self.objTSFMDB.closeDB()
                time.sleep(self.intCheckInterval)
                
        except Exception as error:
            objLogger.error(error, exc_info=True)
            self.objTSFMDB.closeDB()
            