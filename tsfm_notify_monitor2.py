# -*- coding: UTF-8 -*-
import threading, time, json, os
from datetime import datetime
import requests
import NDDB
from config import IPPORT, basedir

intMonitorInterval = 300
intWatchInterval = 5
strSolarModel = 'SolarPW'

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
        threading.Thread.__init__(self)
        self.daemon = True
        self.intCheckInterval = intInterval
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
                #print('find ON user',listResults)
                # uuid,name,model,online_status,gw_uuid,user_id,associated,target_energy_level,lower_bound,start_time,end_time,notify
                
                for listDevice in listResults:
                    #print(listDevice)
                    objNow = datetime.now()
                    intCurrentHour = int(objNow.strftime("%H"))
                    
                    if intCurrentHour >= listDevice[9] and intCurrentHour <= listDevice[10]: # Time period to check power
                        intTimeStamp_Now = int(objNow.timestamp()*1000)
                        strFrom = objNow.strftime("%Y-%m-%d 00:00:00")
                        objFrom = datetime.strptime(strFrom,"%Y-%m-%d %H:%M:%S")
                        intTimeStamp_Start = int(objFrom.timestamp()*1000)
                        
                        litResults = self.objTSFMDB.query(self.strSQL_QueryValue % (strSolarModel,listDevice[0],intTimeStamp_Start,intTimeStamp_Now))
                        #print('litResults',litResults)
                        if litResults != []:
                            if litResults[0][0] is not None:
                                #print('litResults[0][0]',litResults[0][0],'litResults[-1][0]',litResults[-1][0])
                                if (litResults[0][0] - litResults[-1][0]) < listDevice[7] * (listDevice[8]/100):
                                #if (litResults[0][0] - litResults[-1][0]) >= listDevice[7] * (listDevice[8]/100): # for testing
                                    #print('call post...')
                                    
                                    # call notify when sum(value) below the criteria
                                    objResponse = requests.post(strURL_ServiceStore + strPath_Post % listDevice[5], 
                                                                data = json.dumps(self._gen_post(listDevice)), 
                                                                headers = dicHeader)
                                    #print('Send notify:',objResponse,objResponse.content)
                                    #print()
                                    
                                    """
                                    print(listDevice[5])
                                    objResponse = requests.get(strURL_ServiceStore + '/v1/users/%s' % listDevice[5], headers = dicHeader2)
                                    print('get user data:',objResponse,objResponse.content)
                                    print()
                                    """
                #print('outside of for loop')
                time.sleep(self.intCheckInterval)
                #raise Exception('thread is dead!')
                #break
        
        except Exception as error:
            print('Error in monitor thread:',error)
            self.objTSFMDB.closeDB()
            
            
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
            
            for listDevice in listResults:
                #print(listDevice)
                objNow = datetime.now()
                intCurrentHour = int(objNow.strftime("%H"))
                
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
                    if listResults != []:
                        if listResults[0][0] is not None:
                            if (listResults[0][0] - listResults[-1][0]) < listDevice[7] * (listDevice[8]/100):
                            #if (listResults[0][0] - listResults[-1][0]) >= listDevice[7] * (listDevice[8]/100): # for testing
                                #print('call post...')
                                # call notify when sum(value) below the criteria
                                
                                objResponse = requests.post(strURL_ServiceStore + strPath_Post % listDevice[5], 
                                                            data = json.dumps(gen_post_sqlite3(listDevice)), 
                                                            headers = dicHeader)
                                #print('Send notify:',objResponse,objResponse.content)
                                #print()                                    
            
            objConn.close()
            time.sleep(intMonitorInterval)
            #raise Exception('thread is dead!')
            #break
                    
    except Exception as error:
        print(error)
    

if __name__ == '__main__':
    # check system setting
    strEnv = os.getenv('FLASK_CONFIG')
    
    # for testing
    #strEnv = 'testing'
    #basedir = os.path.abspath(os.path.dirname(__file__))
    
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
                time.sleep(intWatchInterval)
                
        except Exception as error:
            print('Main gets error:',error)
        
    else:
        notify_with_sqlite()


    print('Notify monitor is down....')