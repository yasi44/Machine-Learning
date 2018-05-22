# -*- coding: utf-8 -*-
"""
Created on Fri May  4 08:41:52 2018

@author: yasi
"""
import signal
import json
import os
#from kafka import KafkaConsumer, KafkaProducer
import sys
import stock_prediction_model
import threading,logging, time
from stock_prediction_model import StockPrediction
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
import json
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

import warnings
warnings.filterwarnings("ignore")

new_process_flag=False
pid=0

def schedul_kill():
    pid=os.getpid()
    os.kill(pid, signal.SIGTERM) # it kill both parent and child process
    
def main():
    
    new_process_flag=False
    File=open("stockLabels2.labels","r")
    List=[""]
    for Line in File:
        List.append(string.replace(Line,'\n',''))
        

    result =False
    path=os.path.join('','savedMagpieModels')
    
    today= datetime.now().weekday()
    curr_min=datetime.now().minute
    curr_hour=datetime.now().hour    
    stock_pred = StockPrediction()
    labels=List
    print('model loaded')
   
    my_file=open('data2/noline3/2018-03-23-09-18-00.txt','r')
    message=my_file.read()
    
    sched = Scheduler()
    sched.start()        # start the scheduler
    
    #sched.add_cron_job(schedul_func, month='1-12', day_of_week=str((today+6)%7), hour=3, minute=15)
    #for test
    sched.add_cron_job(schedul_kill, month='1-12', day_of_week=str(today), hour='0-23', minute=curr_min+2, second=4)
    
    print('listening to kafka ...')
    while True:      
      sys.stdout.flush()     
      json_stock_prediction =stock_pred.run(message, 0.5)
      #with open('json_stock_prediction.json','w') as outfile:
      #    json.dump(json_stock_prediction,outfile, indent=4, sort_keys=True)
      time.sleep(5)
        
        
if __name__ == "__main__":
   main()
