# -*- coding: UTF-8 -*-
'''
Created on Mar 22, 2022

@author: shawn
'''
import logging, time
from datetime import datetime, timedelta

strScope_TotalPower = 'generatedElectricity'
int1stDateOfWeek = 0 # Monday

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
    
    def update(self,strSQLCmd,listData):
        try:
            objCursor = self.objDB.cursor()
            objCursor.execute(strSQLCmd % tuple(listData))
            self.objDB.commit()
        except (Exception) as error:
            objLogger.error("Error while updating!\n%s" % error)
            #print('Error when querying DB: ',error)
            self.close()
        
    def close(self):
        self.objDB.close()


def if_last_day_of_month(objToday):
    next_month = objToday.replace(day=28) + timedelta(days=4)
    objLastDay = next_month - timedelta(days=next_month.day)
    if objLastDay.strftime("%d") == objToday.strftime("%d"):
        return True
    else:
        return False
    

def update_period_data(strDBType,objDB,strModels,intTimeZoneHour):
    
    if strDBType == 'sqlite':
        objDB2 = Sqlite3DB(objDB)
    else:
        objDB2 = objDB
    
    try:        
        objNow = datetime.now()
        objNewDateTime = objNow + timedelta(hours=intTimeZoneHour)
        intCurrentHour = int(objNewDateTime.strftime("%H"))
        if intCurrentHour == 23:
        #if intCurrentHour > 0: # for testing
            intTimeStamp_MidNight23Hour = int(objNow.timestamp()*1000)
            #intTimeStamp_MidNight23Hour = 1647925628699 # for testing
            listDeviceInfoResults = objDB2.query("select uuid, weekly_energy_amount, monthly_energy_amount, annual_energy_amount from device_info where model in %s" % strModels)
            for listDevice in listDeviceInfoResults:
                # Read the value of today's last generated power
                listGenPower = objDB2.query("select value, generated_time from device_data where dev_uuid = '%s' and scope = 'generatedElectricity' and generated_time < %s order by generated_time desc LIMIT 1" % (listDevice[0],intTimeStamp_MidNight23Hour))
                if listGenPower != []:
                    intWeekDay = datetime.today().weekday() # 0 (monday), .......
                    if intWeekDay == 6: # Sunday night
                        floatWeeklyAmount = 0 # reset for the total of this week
                    else:
                        floatWeeklyAmount = listDevice[1] + listGenPower[0][0]
                    if if_last_day_of_month(datetime.today()):
                        floatMonthlyAmount = 0 # reset for the total of this month
                    else:
                        floatMonthlyAmount = listDevice[2] + listGenPower[0][0]
                    if objNow.strftime("%m-%d") == '12-31':
                        floatAnnualAmount = 0 # reset for the total of this year
                    else:
                        floatAnnualAmount = listDevice[3] + listGenPower[0][0]
                    objLogger.debug('floatWeeklyAmount: '+ str(floatWeeklyAmount))
                    objLogger.debug('floatMonthlyAmount: '+ str(floatMonthlyAmount))
                    objLogger.debug('floatAnnualAmount: '+ str(floatAnnualAmount))
                    objDB2.update("update device_info set weekly_energy_amount = %s, monthly_energy_amount = %s, annual_energy_amount = %s where uuid = '%s'", [floatWeeklyAmount,floatMonthlyAmount,floatAnnualAmount,listDevice[0]])
                    time.sleep(1)
    
    except Exception as error:
        objLogger.error(error, exc_info=True)


if __name__ == '__main__':
    pass
    