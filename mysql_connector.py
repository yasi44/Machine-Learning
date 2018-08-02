# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 13:30:23 2018

@author: yasi
"""
from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta



class MYSQLConnector:
    def __init__(self,username='root', password='1234',host='127.0.0.1',database=None):
        self.cnx = None
        self.cursor = None
#        self.cnx.database= None        
        try:
            self.cnx = mysql.connector.connect(user=username,password=password,host=host,database=database)
            self.cursor = self.cnx.cursor()
            print("connection created")
#            self.cnx.database = database
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                try:
                    self.cursor.execute(
                        "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database))
                except mysql.connector.Error as err:
                    print("Failed creating database: {}".format(err))
                    exit(1)
#                self.cnx.database = database
            else:
                print(err)
        else:
            self.cnx.close()
      
    def __del__(self):
        self.cursor.close()
        self.cnx.close()
         
   
    def create_table(self,list_tables):
        for name, ddl in list_tables.iteritems():
            try:
                print("Creating table {}: ".format(name), end='')
                self.cursor.execute(ddl)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
                
    def execute_query(self, query, values):
        self.cursor.execute(query, values)
        self.cnx.commit()

    
