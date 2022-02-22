# -*- coding: UTF-8 -*-
'''
Created on Oct 8, 2021

@author: shawn 
'''
import psycopg2, logging
from psycopg2 import Error

objLogger = logging.getLogger(__name__)

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
            objLogger.info('NDDB is connected!')
            
        except (Exception, psycopg2.DatabaseError) as error:
            objLogger.error("Error while connecting to NDDB!\n%s" % error)
                    
    
    def query(self,strSQLCmd):
        try:
            self.objCursor.execute(strSQLCmd)
            return self.objCursor.fetchall() # list
        except (Exception, psycopg2.DatabaseError) as error:
            objLogger.error("Error while querying!\n%s" % error)
            self.closeDB()
        
    
    def update(self,strSQLCmd):
        try:
            self.objCursor.execute(strSQLCmd)
            self.objConn.commit()
            objLogger.info('DB update successfully...')
        except (Exception, psycopg2.DatabaseError) as error:
            objLogger.error("Error while inserting!\n%s" % error)
            self.closeDB()
            
            
    def delete(self,strSQLCmd):
        try:
            self.objCursor.execute(strSQLCmd)
            self.objConn.commit()
            objLogger.info('Deleting data successfully...')
            objLogger.info("Total number of rows deleted : %s" % self.objCursor.rowcount)
        except (Exception, psycopg2.DatabaseError) as error:
            objLogger.error("Error while deleting!\n%s" % error)
            self.objCursor.close()
            self.objConn.close()
            
            
    def closeDB(self):
        self.objCursor.close()
        self.objConn.close()
        objLogger.info('NDDB connection is closed!')
        
    