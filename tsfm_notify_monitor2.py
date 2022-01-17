# -*- coding: UTF-8 -*-
import threading, time, json, os, requests, logging
from datetime import datetime, timedelta
import NDDB, NDLogger
from config import IPPORT, basedir

intMonitorInterval = 300
intWatchInterval = 5
strSolarModel = 'SolarPW'
intTimeZoneHour = 8

dicTSFM_DB = {
    'strHost':'192.168.7.85',
    'strPort':'5432',
    'strUser':'postgres',
    'strPW':'link4581',
    'strDB':'TEST'
    }

strURL_ServiceStore = 'https://store-api-qa.nextdrive.io'
strPath_Post = '/v1/users/%s/posts' # {ssUserId}

dicHeader = {
    'X-ND-TOKEN':'qt5pOgkyHX3SqxqzfvN/ADVAg3KbV5zrWIXbM8H',
    'Content-Type':'application/json'
    }

dicHeader2 = {
    'accept': '*/*'
    }

strDB_Test = 'data-test.sqlite'

class monitor(threading.Thread):
    def __init__(self,strDBType,intInterval):
        objLogger.debug('Init Monitor class...')
        threading.Thread.__init__(self)
        self.daemon = True
        self.intCheckInterval = intInterval
        objLogger.debug('DB Type: %s' % strDBType)
        if strDBType == 'production':
            self._conn_postgres_db()
        elif strDBType == 'testing':
            self._conn_sqlite3_db()
        
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
        
        self.strSQL_FindUser_ON = "select * from public.device_info where model = '%s' and notify = 'ON'"
        self.strSQL_QueryValue = """select value,generated_time from public.device_data where 
        model = '%s' and scope = 'generatedElectricity' and dev_uuid = '%s' and 
        generated_time >= %s and generated_time <= %s 
        order by generated_time desc
        """
    
    def _gen_post(self,listDev):
        # uuid,name,model,online_status,gw_uuid,user_id,associated,target_energy_level,lower_bound,start_time,end_time,notify
        strIP = IPPORT
        #strIP = '755c-118-163-111-169.ngrok.io' # testing
        dicNotify = {
            "format": 1,
            "name": "NextDrive TSFM",
            "icon": "https://%s/postpicture/SolarPanel.png" % strIP,
            "title": "發電低下通知",
            "description": "太陽能發電模組, %s, 發電量低於通知設定" % listDev[1],
            "images": [
                    {
                        "previewImageUrl": "https://%s/postpicture/LowSellingPower.png" % strIP,
                        "originalContentUrl": "https://%s/postpicture/LowSellingPower.png" % strIP
                    }
                ],
            "contents": []
        }
        return dicNotify
    
    def run(self):
        #self.strThreadID = threading.get_ident()
        try:
            while True:
                # find users and devices that notify = ON
                listResults = self.objTSFMDB.execute(self.strSQL_FindUser_ON % strSolarModel)
                #objLogger.debug('find ON user: %s' % str(stResults))
                #print('find ON user',listResults)
                # uuid,name,model,online_status,gw_uuid,user_id,associated,target_energy_level,lower_bound,start_time,end_time,notify
                
                for listDevice in listResults:
                    #print(listDevice)
                    objLogger.debug('listDevice: %s' % str(listDevice))
                    objNow = datetime.now()
                    objNewDateTime = objNow + timedelta(hours=intTimeZoneHour)
                    intCurrentHour = int(objNewDateTime.strftime("%H"))
                    
                    if intCurrentHour >= listDevice[9] and intCurrentHour <= listDevice[10]: # Time period to check power
                        intTimeStamp_Now = int(objNow.timestamp()*1000)
                        strFrom = objNow.strftime("%Y-%m-%d 00:00:00")
                        objFrom = datetime.strptime(strFrom,"%Y-%m-%d %H:%M:%S")
                        intTimeStamp_Start = int(objFrom.timestamp()*1000)
                        
                        litResults = self.objTSFMDB.query(self.strSQL_QueryValue % (strSolarModel,listDevice[0],intTimeStamp_Start,intTimeStamp_Now))
                        #print('litResults',litResults)
                        objLogger.debug('litResults: %s' % str(litResults))
                        if litResults != []:
                            if litResults[0][0] is not None:
                                #print('litResults[0][0]',litResults[0][0],'litResults[-1][0]',litResults[-1][0])
                                objLogger.debug('litResults[0][0]: %s' % litResults[0][0])
                                objLogger.debug('litResults[-1][0]: %s' % litResults[-1][0])
                                if (litResults[0][0] - litResults[-1][0]) < listDevice[7] * (listDevice[8]/100):
                                #if (litResults[0][0] - litResults[-1][0]) >= listDevice[7] * (listDevice[8]/100): # for testing
                                    #print('call post...')
                                    
                                    # call notify when sum(value) below the criteria
                                    objResponse = requests.post(strURL_ServiceStore + strPath_Post % listDevice[5], 
                                                                data = json.dumps(self._gen_post(listDevice)), 
                                                                headers = dicHeader)
                                    #print('Send notify:',objResponse,objResponse.content)
                                    #print()
                                    objLogger.debug('Send notify: %s, %s' % (objResponse,objResponse.content))
                                    objLogger.debug('')
                                    
                                    """
                                    print(listDevice[5])
                                    objResponse = requests.get(strURL_ServiceStore + '/v1/users/%s' % listDevice[5], headers = dicHeader2)
                                    print('get user data:',objResponse,objResponse.content)
                                    print()
                                    """
                time.sleep(self.intCheckInterval)
                #raise Exception('thread is dead!')
                #break
        
        except Exception as error:
            print('Error in monitor thread:',error)
            objLogger.error(error, exc_info=True)
            self.objTSFMDB.closeDB()
            objLogger.info('Close DB')
            
            
def gen_post_sqlite3(listDev):
    # uuid,name,model,online_status,gw_uuid,user_id,associated,target_energy_level,lower_bound,start_time,end_time,notify
    strIP = IPPORT
    #strIP = '755c-118-163-111-169.ngrok.io' # testing
    dicNotify = {
        "format": 1,
        "name": "NextDrive TSFM",
        "icon": "https://%s/postpicture/SolarPanel.png" % strIP,
        "title": "發電低下通知",
        "description": "太陽能發電模組, %s, 發電量低於通知設定" % listDev[1],
        "images": [
                {
                    "previewImageUrl": "https://%s/postpicture/LowSellingPower.png" % strIP,
                    "originalContentUrl": "https://%s/postpicture/LowSellingPower.png" % strIP
                }
            ],
        "contents": []
    }
    return dicNotify

def notify_with_sqlite():
    # since sqlite3 cannot be run in different threads, we cannot use the same method as Postgresql DB module.
    import sqlite3
    
    try:
        while True:
            # connect to sqlite3 DB
            # find users and devices that notify = ON
            objConn = sqlite3.connect(os.path.join(basedir,strDB_Test))
            objCursor = objConn.execute("select * from device_info where model = '%s' and notify = 'ON'" % strSolarModel)
            listResults = objCursor.fetchall()
            #objLogger.debug('listResults: %s' % str(listResults))
            for listDevice in listResults:
                #print(listDevice)
                objLogger.debug('listDevice: %s' % str(listDevice))
                objNow = datetime.now()
                objNewDateTime = objNow + timedelta(hours=intTimeZoneHour)
                intCurrentHour = int(objNewDateTime.strftime("%H"))
                
                if intCurrentHour >= listDevice[9] and intCurrentHour <= listDevice[10]: # Time period to check power
                    intTimeStamp_Now = int(objNow.timestamp()*1000)
                    strFrom = objNow.strftime("%Y-%m-%d 00:00:00")
                    objFrom = datetime.strptime(strFrom,"%Y-%m-%d %H:%M:%S")
                    intTimeStamp_Start = int(objFrom.timestamp()*1000)
                    
                    strSQL = """select value,generated_time from device_data where 
                    model = '%s' and scope = 'generatedElectricity' and dev_uuid = '%s' and 
                    generated_time >= %s and generated_time <= %s 
                    order by generated_time desc
                    """
                    objCursor = objConn.execute(strSQL % (strSolarModel,listDevice[0],intTimeStamp_Start,intTimeStamp_Now))
                    listResults = objCursor.fetchall()
                    #print('listResults',listResults)
                    objLogger.debug('listResults: %s' % str(listResults))
                    if listResults != []:
                        if listResults[0][0] is not None:
                            objLogger.debug('litResults[0][0]: %s' % listResults[0][0])
                            objLogger.debug('litResults[-1][0]: %s' % listResults[-1][0])
                            if (listResults[0][0] - listResults[-1][0]) < listDevice[7] * (listDevice[8]/100):
                            #if (listResults[0][0] - listResults[-1][0]) >= listDevice[7] * (listDevice[8]/100): # for testing
                                #print('call post...')
                                objLogger.debug('call post...')
                                # call notify when sum(value) below the criteria
                                
                                objResponse = requests.post(strURL_ServiceStore + strPath_Post % listDevice[5], 
                                                            data = json.dumps(gen_post_sqlite3(listDevice)), 
                                                            headers = dicHeader)
                                #print('Send notify:',objResponse,objResponse.content)
                                #print()                                    
                                objLogger.debug('Send notify: %s, %s' % (objResponse,objResponse.content))
                                objLogger.debug('')
            
            objConn.close()
            time.sleep(intMonitorInterval)
            #raise Exception('thread is dead!')
            #break
                    
    except Exception as error:
        print(error)
        objLogger.error(error, exc_info=True)
    

if __name__ == '__main__':
    
    # init debug log
    strCurrentPath = os.path.dirname(os.path.realpath(__file__))
    strLogFile = datetime.now().strftime("TSFM_Notify_%Y%m%d_%H%M%S")
    NDLogger.Logger(strLogFile,strCurrentPath)
    objLogger = logging.getLogger('tsfm_notify_monitor2')
    objLogger.info('TSFM Notify Monitor starts....')
    
    # check system setting
    strEnv = os.getenv('FLASK_CONFIG')
    
    # for testing
    strEnv = 'testing'
    basedir = os.path.abspath(os.path.dirname(__file__))    
    
    if strEnv == 'production':
        try:
            thdMonitor = monitor(strEnv,intMonitorInterval)
            thdMonitor.start()
            time.sleep(1)
            while True:
                #break
                if not thdMonitor.is_alive():
                    thdMonitor = monitor(strEnv,intMonitorInterval)
                    thdMonitor.start()
                    time.sleep(1)
                #print('monitor thread id:',thdMonitor.get_thread_ID())
                objLogger.info('Re-launch monitor thread id:',thdMonitor.get_thread_ID())
                time.sleep(intWatchInterval)
                
        except Exception as error:
            print('Main gets error:',error)
            objLogger.error('Main gets error:',error)
        
    else:
        notify_with_sqlite()

    objLogger.info('Notify monitor is down....')
    print('Notify monitor is down....')