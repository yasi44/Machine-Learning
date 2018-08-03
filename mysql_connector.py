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
    
    def __init__(self,username, password,host,database):
#        self.cnx = None
#        self.cursor = None
        self.username=username
        self.password=password
        self.host=host
        self.database=database
        try:
            self.cnx = mysql.connector.connect(user=self.username,password=self.password,host=self.host,database=self.database)
            print("successfully connected to db")
            self.cnx.database=self.database
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("DB does not exist")
                self.create_database()
                self.cnx.database = self.database
                print("DB created")
            elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            else:
                print(err)

    def __del__(self):
        self.cursor.close()
        self.cnx.close()
        
    def create_database(self):
        try:
            print("connecting...")            
            self.cnx = mysql.connector.connect(user=self.username,password=self.password,host=self.host)
            print("connection created")
            self.cursor = self.cnx.cursor()
            print(self.database)
            self.cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.database))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
          
    def create_table(self,list_tables):
        for name, ddl in list_tables.iteritems():
            try:
                print("Creating table {}: ",name)
                self.cursor.execute(ddl)
                print("created")
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
                
    def select_query(self, query):
        try:
            self.cursor.execute(query)
            print("query executed")
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
            myresult = self.cursor.fetchall()
            for x in myresult:
              print(x)
            
    def insert_query(self, query,values):
        try:
            self.cursor.execute(query,values)
            print("query executed")
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
            self.cnx.commit()
