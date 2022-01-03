# -*- coding: UTF-8 -*-
'''
Created on Oct 8, 2021

@author: shawn
'''
import psycopg2
from psycopg2 import Error

class NDDB(object):
    '''
    The class to access DB of ND QA staging
    '''
    def __init__(self,strHost,strPort,strUser,strPW,strDatabase):
        self._conn2db(strDatabase,strHost,strPort,strUser,strPW)
        
        
    def _conn2db(self,strDB,strURL,strPort,strID,strPW):
        try:
            self.objConn = psycopg2.connect(user=strID,
                                            password=strPW,
                                            host=strURL,
                                            port=strPort,
                                            database=strDB)
            self.objCursor = self.objConn.cursor()
            print('NDDB is connected!')
            
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to NDDB!", error)
        finally:
            print()
        
    
    def query(self,strSQLCmd):
        try:
            self.objCursor.execute(strSQLCmd)
            return self.objCursor.fetchall() # list
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while querying!", error)
            self.closeDB()
        
    
    def update(self,strSQLCmd):
        try:
            self.objCursor.execute(strSQLCmd)
            self.objConn.commit()
            print('DB update successfully...')
            print()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while inserting!", error)
            self.closeDB()

            
    def closeDB(self):
        self.objCursor.close()
        self.objConn.close()
        print("NDDB connection is closed!")
        
    