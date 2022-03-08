# -*- coding: UTF-8 -*-
'''
Created on Mar 4, 2022

@author: shawn
'''
from monitor.gen_post import GenPosts
import logging, requests, json

objLogger = logging.getLogger(__name__)

class Sqlite3DB(object):
    '''
    The class to access sqlite3 DB
    '''
    def __init__(self,objDB):
        self.objDB = objDB
        
    def query(self,strSQLCmd):
        try:
            objCursor = self.objDB.execute(strSQLCmd)
            return objCursor.fetchall() # list
        except (Exception) as error:
            objLogger.error("Error while querying!\n%s" % error)
            #print('Error when querying DB: ',error)
            self.close()
    
    def close(self):
        self.objDB.close()

        
def find_group_diff(strDBType,objDB,strModels,objNotify,strCheckingInterval):
    if strDBType == 'sqlite':
        objDB2 = Sqlite3DB(objDB)
    else:
        objDB2 = objDB
    
    listDeviceInfoResults = objDB2.query("select user_id, group_id, uuid, group_lower_bound from device_info where model in %s and online_status = 'ONLINE' order by user_id, group_id" % strModels)
    #listResults = objDB2.query("select user_id, group_id from device_info where model in %s and online_status = 'ONLINE' order by user_id, group_id" % strModels)
    #print('first query:\n', listResults)
    dicUserGroups = {}
    listTemp = []
    strLastUser = ''
    for listUserGroup in listDeviceInfoResults:
        if listUserGroup[0] != strLastUser:
            listTemp = []
        listTemp.append(listUserGroup[1])
        dicUserGroups[listUserGroup[0]] = list(set(listTemp))
        strLastUser = listUserGroup[0]
    #print(dicUserGroups) #{'94f43ded-55b6-4354-aaae-c5cc20fde280': ['1', '2'], '94f43ded-55b6-4354-aaae-c5cc20fde281': ['1']}
    
    for strUser, listGroups in dicUserGroups.items():
        for strGroup in listGroups:
            #listResults = objDB2.query("select uuid, group_lower_bound from device_info where user_id = '%s' and group_id = '%s' order by group_id" % (strUser,strGroup))       
            listResults = []
            for listDevice in listDeviceInfoResults:
                listTemp = []
                if listDevice[0] == strUser and listDevice[1] == strGroup:
                    listTemp.append(listDevice[2]) # device uuid
                    listTemp.append(listDevice[3]) # group_lower_bound
                listResults.append(listTemp)
            #print("listResults",listResults)
            intGroupLowBond = listResults[0][1] # I do not check if one of low-bond value is different from others in the same group
            listInstancePower = []
            for listDeviceLowBond in listResults:
                listResults = objDB2.query("select value, generated_time from device_data where dev_uuid = '%s' and scope = 'instanceElectricity' order by generated_time desc LIMIT 1" % listDeviceLowBond[0])
                #print(listResults)
                listInstancePower.append(int(listResults[0][0]*1000))
                #print('listInstancePower',listInstancePower)
                                
            listInstancePower.sort(reverse = True)
            #print(listInstancePower)
            #print("listInstancePower[0] - listInstancePower[-1]: ", listInstancePower[0] - listInstancePower[-1])
            objLogger.debug("listInstancePower: " + str(listInstancePower))
            objLogger.debug("listInstancePower[0] - listInstancePower[-1]: " + str(listInstancePower[0] - listInstancePower[-1]))
            if listInstancePower[0] - listInstancePower[-1] > intGroupLowBond:
                objLogger.debug('call STWrongInGroup post...')
                
                # strGroup, strMin
                dicPost = objNotify.STWrongInGroup(strGroup,strCheckingInterval)
                objResponse = requests.post(objNotify.strURL_ServiceStore + objNotify.strPath_Post % strUser, 
                                            data = json.dumps(dicPost), 
                                            headers = objNotify.dicHeader)
                objLogger.debug('Send notify: %s, %s' % (objResponse,objResponse.content))
                #print('Send notify: %s, %s' % (objResponse,objResponse.content))
                
                objLogger.debug('')
         
            
if __name__ == '__main__':
    pass
    