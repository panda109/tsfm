# -*- coding: UTF-8 -*-
'''
Created on Feb 10, 2022

@author: shawn
'''
from app.main.language import Language
from config import IPPORT

class GenPosts(object):
    def __init__(self, strLang):
        self.strHost = IPPORT
        if strLang.lower() == 'zh_tw':
            self.dicMsgs = Language.clanguage
        else:
            self.dicMsgs = Language.elanguage
        
        self.strURL_ServiceStore = 'https://store-api-qa.nextdrive.io'
        self.strPath_Post = '/v1/users/%s/posts' # {ssUserId}
        self.dicHeader = {            
            'X-ND-TOKEN':'qt5pOgkyHX3SqxqzfvN/ADVAg3KbV5zrWIXbM8H',
            'Content-Type':'application/json'
            }        
        
    def LowPowerGeneration(self, strPVName, strStartTime, strEndTime, intTotal, intTargetTotal, intTargetPercent):
        dicNotify = {
            "format": 1,
            "name": "NextDrive 太陽能發電監視服務",
            "icon": "http://%s/postpicture/SolarPanel.png" % self.strHost,
            "title": self.dicMsgs['PST_01_01'],
            # "太陽能發電模組 %s，今日 %s ~ %s 發電量： %s kWh。低於 %s kWh 的 %s%。"
            "description": self.dicMsgs['PST_01_02'] % (strPVName, strStartTime, strEndTime, intTotal, intTargetTotal, intTargetPercent),
            "images": [
                    {
                        "previewImageUrl": "http://%s/postpicture/post_LowSellingPower.png" % self.strHost,
                        "originalContentUrl": "http://%s/postpicture/post_LowSellingPower.png" % self.strHost
                    }
                ],
            "contents": []
        }
        return dicNotify
        
    def NoPowerGeneration(self, strPVName, strMin):
        dicNotify = {
            "format": 1,
            "name": "NextDrive 太陽能發電監視服務",
            "icon": "http://%s/postpicture/SolarPanel.png" % self.strHost,
            "title": self.dicMsgs['PST_02_01'],
            # 太陽能發電模組 %s，過去 %s 分鐘內發電狀況異常，請檢查設備狀態。
            "description": self.dicMsgs['%PST_02_02'] % (strPVName, strMin),
            "images": [
                    {
                        "previewImageUrl": "http://%s/postpicture/post_NoPower.png" % self.strHost,
                        "originalContentUrl": "http://%s/postpicture/post_NoPower.png" % self.strHost
                    }
                ],
            "contents": []
        }
        return dicNotify
        
        
