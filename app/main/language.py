# _*_ coding: utf_8 _*_
'''
Created on 2022年1月19日

@author: automan
'''

class Language(object):
    
    clanguage = {
        'PV_01_01'    :    "通知方法設定",
        'PV_01_02'    :    "通知  OFF/ON",
        'PV_01_03'    :    "通知",
    
        'PV_01_04'    :    "尚無配對的太陽能板。請先完成裝置的配對。",
    
        'PV_01_05'    :    "儲存",
        'PV_01_06'    :    "根據設定的時間每小時發送一次通知。",
        'PV_01_07'    :    "目標量",
        'PV_01_08'    :    "請輸入1~9,999的數字。",
        'PV_01_09'    :    "低於該值時通知",
        'PV_01_10'    :    "開始時間",
        'PV_01_11'    :    "結束時間",
        'PV_01_12'    :    "完成",
        'PV_01_13'    :    "瓩⋅時",
        
        'PST_01_01'   :    "發電低下通知",
        'PST_01_02'   :    "太陽能發電模組 %s，今日 %s ~ %s 發電量： %s kWh。低於 %s kWh 的 %s%。",
        'PST_02_01'   :    "發電異常通知",
        'PST_02_02'   :    "太陽能發電模組 %s，過去 %s 分鐘內發電狀況異常，請檢查設備狀態。"
        }
    
    elanguage = {
        'PV_01_01' :   'PV Generation Alert',
        'PV_01_02' :   'Notification OFF/ON',
        'PV_01_03' :   'Notification',
        'PV_01_04' :   'There are no paired solar panels yet. Please complete the pairing of the appliance first.',
        'PV_01_05' :   'Save',
        'PV_01_06' :   'Send notifications every hour based on a set time.',
        'PV_01_07' :   'Goal',
        'PV_01_08' :   'Please enter a number between 1~9,999 kWh.',
        'PV_01_09' :   'Lower Bound',
        'PV_01_10' :   'Starting Time',
        'PV_01_11' :   'End Time',
        'PV_01_12' :   'Done',
        'PV_01_13' :  'kWh',
        'PST_01_01' :  'Low power generation notification',
        'PST_01_02' :  "Today %s ~ %s power generation: %s kWh. Below %s% of %s kWh.",
        'PST_02_01' :  'Abnormal power generation notification',
        'PST_02_02' :  'Abnormal power generation in the past %s minutes, please check your equipments.'
        }
        
    jlanguage = {
        'PV_01_01'    :    "通知方法設定",
        'PV_01_02'    :    "通知  OFF/ON",
        'PV_01_03'    :    "通知",
    
        'PV_01_04'    :    "尚無配對的太陽能板。請先完成裝置的配對。",
    
        'PV_01_05'    :    "儲存",
        'PV_01_06'    :    "根據設定的時間每小時發送一次通知。",
        'PV_01_07'    :    "目標量",
        'PV_01_08'    :    "請輸入1~9,999的數字。",
        'PV_01_09'    :    "低於該值時通知",
        'PV_01_10'    :    "開始時間",
        'PV_01_11'    :    "結束時間",
        'PV_01_12'    :    "完成",
        'PV_01_13'    :    "瓩⋅時",
        
        'PST_01_01'   :    "發電低下通知",
        'PST_01_02'   :    "今日 %s ~ %s 發電量： %s kWh。低於 %s kWh 的 %s%。",
        'PST_02_01'   :    "發電異常通知",
        'PST_02_02'   :    "過去 %s 分鐘內發電狀況異常，請檢查設備狀態。"
        }

    def __init__(self):
        '''
        Constructor
        '''
        