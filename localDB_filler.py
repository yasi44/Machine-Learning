# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 15:08:54 2018

@author: yasi

to store cleaned text (after stemming and removing stopwords in my local db)
"""

import requests
from bs4 import BeautifulSoup
import requests
from bs4 import *
from datetime import datetime
import time
from apscheduler.scheduler import Scheduler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import gmtime, strftime, timezone
import pytz
import datetime as dt
from dateutil.tz import gettz
import datetime
import exception_handling
from config_manager import ConfigManager
from exception_handling import PrintException
from mysql_connector import MYSQLConnector
from text_clean import normal_txt_clean
 
    
       
"""       
all configuration are set in .config file in data_files

"""
import re
import shutil
import os
from bs4 import *
import time
from magpie import Magpie
from elasticsearch import Elasticsearch
import string
from datetime import datetime
import mysql.connector as msc #for py2.7
from datetime import timedelta
from text_clean import clean_write
from exception_handling import PrintException
from mysql_connector import MYSQLConnector
#import mysqlclient # for py 3

   
class LocalDBFiller:
    def __init__(self,configs,input_param):
        try:
            tokens_pre=[]
            tokens_curr=[]
            tokens_pre=input_param[0].split("-")
            pre_time = datetime(int(tokens_pre[0]), int(tokens_pre[1]), int(tokens_pre[2]), int(tokens_pre[3]), int(tokens_pre[4]),int(tokens_pre[5]) )       
            tokens_curr=input_param[1].split("-")
            curr_time = datetime(int(tokens_curr[0]), int(tokens_curr[1]), int(tokens_curr[2]), int(tokens_curr[3]), int(tokens_curr[4]),int(tokens_curr[5]))
            self.elastic_prev_time=int(pre_time.strftime("%s"))*1000 #to be in millisecond instead of second(javascript version of unix time)
            self.elastic_curr_time=int(curr_time.strftime("%s"))*1000 #to be in millisecond instead of second(javascript version of unix time)
            self.config_obj=configs
            # get from elastic
            self.MYSQLobj=MYSQLConnector(configs.get_sqlconfig_user(),configs.get_sqlconfig_pass(),configs.get_sqlconfig_host(),configs.get_sqlconfig_cleanedNewsdb())
            #                config_obj=ConfigManager()
            TABLES = {}
            TABLES['afterStemStop'] = (
            "CREATE TABLE `afterStemStop` ("
            "`news_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
            "`published_date` datetime NOT NULL, "
            "`clean_content` VARCHAR(3000)" 
            ") ENGINE=InnoDB")            
            self.MYSQLobj.create_table(TABLES)
            self.MYSQLobj.commit()
            self.insert_query='INSERT INTO afterStemStop(published_date,clean_content) VALUES (%s,%s)'
            self.check_existance_query='SELECT * FROM afterStemStop WHERE published_date=%s'
            
        except Exception as e:
            PrintException(e, exitStatus=True)        
        
    
    # to get the latest news from elastic   
    def grabber_cleaner(self):

#        print("news_stockprice_gap: "+str(self.config_obj.get_news_stockprice_gap()))
        try:
            print("grabber_cleaner...")

#            now=datetime.now() 
#            #now = datetime(first_pre_time.year, first_pre_time.month, first_pre_time.day, first_pre_time.hour,first_pre_time.minute,first_pre_time.second)
#            curr_time= int(now.strftime("%s"))*1000#to be in millisecond instead of second(javascript version of unix time)
            print("pre_time:%s"%time.ctime(self.elastic_prev_time/1000))    
            es = Elasticsearch()
            elasticsearch = '10.4.130.7:9200'#TODO: to import elasticsearch info in .config
            es = Elasticsearch([elasticsearch])
            index = 'article_v2'
            query = {
              "size": 10000,
              "_source": ["published_date", "content"],
              "query": {
                "bool": {
                  "must_not": [
                    {
                      "match": {
                        "category": "announcement"
                      }
                    }
                  ],
            		"must": [
                    {"range": 
            			{
            				"published_date": {
            					"gte": self.elastic_prev_time,
            					"lte": self.elastic_curr_time,
            					"format": "epoch_millis"
            				}
            			}
            		}
                  ]
                }
              },
              "sort": [
                {
                  "published_date": {
                    "order": "desc"
                  }
                }
              ]
            }
            res = es.search(index=index, doc_type="_doc", body=query)
            time.sleep(10)
            print("curr_time:%s"%time.ctime(self.elastic_curr_time/1000))
            self.elastic_prev_time = self.elastic_curr_time# no need
           

            print("grabbing news from elastic...")            
            for doc in res['hits']['hits']:
                doc_date=doc['_source']['published_date']
                doc_date_refined=doc_date[:doc_date.find('+')]
                doc_date_refined=doc_date_refined.replace('T','-')
                doc_date_refined=doc_date_refined.replace(':','-')
#                doc_date_refined=doc_date[:doc_date.find('+')]
#                doc_date_refined=doc_date_refined.encode('ascii', 'ignore')
                doc_date=datetime.strptime(doc_date_refined, '%Y-%m-%d-%H-%M-%S')
                doc_date_refined=datetime.strftime(doc_date, '%Y-%m-%d-%H-%M-%S')#vonvert to str. (strptime to datetime)
                
#                doc_date_refined=doc_date_refined.encode('ascii', 'ignore')
                result = self.MYSQLobj.select_query(self.check_existance_query,list(doc_date_refined))
                if (result==None):
                    
#                    doc_date_refined=doc_date_refined.replace(hour=0, minute=0, second=0) 
                    doc_content=doc['_source']['content']
                    doc_content=doc_content.encode('ascii', 'ignore')# limits news to english only
                    cleaned_news=normal_txt_clean(doc_content)#writes in 'elastic_grabbed_news' folder
                    cleaned_news=cleaned_news.encode('ascii', 'ignore')
                    values=[doc_date_refined,cleaned_news]                     
                    self.MYSQLobj.insert_query(self.insert_query,values)
#                    self.MYSQLobj.commit()

            self.MYSQLobj.commit()
            time.sleep(10)
            print('news grabbed, cleaned and put in cleanedNewsdb')
        except Exception as e:
            PrintException(e, exitStatus=True)
 #results=self.MYSQLobj.select_query("SELECT name,chg_percent FROM malaysiaStocksRecords where (record_date between %s and %s)", values=(news_date_time,news_date_time_daley))           

    
   
# from child kafka puller

import signal
import json
import os
#from kafka import KafkaConsumer, KafkaProducer
import sys
import stock_prediction_model
import threading,logging, time
#from auto_model_trainer import LocalDBFiller
from config_manager import ConfigManager # instead save config as .py and load it like: from magpie.config import NN_ARCHITECTURE, BATCH_SIZE, EMBEDDING_SIZE, EPOCHS
#from apscheduler.scheduler import scheduler
import time
from apscheduler.scheduler import Scheduler
import sched
import subprocess # to call jar file inside python
import re
import os
import requests
from bs4 import *
from bs4 import BeautifulSoup
from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import gmtime, strftime, timezone
import pytz
from datetime import datetime
from time import gmtime, strftime
from dateutil.tz import gettz
import json
import csv
from pprint import pprint
import gensim, logging
import collections
import magpie
from magpie import Magpie
import difflib
import keras
import string
import logging
logging.basicConfig()
from queue import Queue
import subprocess
from exception_handling import PrintException
import sys

new_process_flag=False
pid=0

# the created child process will kill itself
def schedul_kill():
    try:
        pid=os.getpid()
        os.kill(pid, signal.SIGTERM) # it kill both parent and child process
    except Exception:
        PrintException()

def main():
    try:
#        input_param=sys.argv
#        print(input_param[1])
#        print(input_param[2])
        #for test only
        p1=datetime.strftime(datetime(2018,9,19,1,1,1), '%Y-%m-%d-%H-%M-%S')
        p2=datetime.strftime(datetime(2018,9,20,1,1,1), '%Y-%m-%d-%H-%M-%S')
        input_param=[p1,p2]
        
        print("loading config file...")
        config_obj=ConfigManager()
        print('creating AutoTrainer object ...')
        localDB_filler_obj = LocalDBFiller(config_obj,input_param)
        localDB_filler_obj.grabber_cleaner()# TODO: decide what todo with output
        time.sleep(5)
        schedul_kill()
    except Exception:
        PrintException()    
        
if __name__ == "__main__":
   main()   
   
   
    
