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

# the created child process will kill itself
def schedul_kill():
    try:
        pid=os.getpid()
        os.kill(pid, signal.SIGTERM) # it kill both parent and child process
    except Exception:
        PrintException()
    
    #subprocess.call('python /home/yasi/Documents/python_codes/tempsTest.py', shell=True) 
    #this one works but opens a subprocess dependent to main process. we want a new independent process    
    #pid=subprocess.Popen(args=["gnome-terminal", "--command=python /home/yasi/Documents/python_codes/tempsTest.py"]).pid
    

def main():

    #for test purpose only
    time_now=datetime.now()
    today= time_now.weekday()
    curr_min=time_now.minute
    my_file=open('data2/noline3/2018-03-23-09-18-00.txt','r')
    message=my_file.read()
    stock_pred = StockPrediction()
    print("loading config file...")
    config_obj=ConfigManager()
    print("config_obj loaded")
    sched = Scheduler()
    sched.start() 
#    sched.add_cron_job(schedul_kill, month='1-12', day_of_week=str(today), hour='0-23', minute=curr_min+4, second=time_now.second+4)
    sched.add_cron_job(schedul_kill, year=2018,month=config_obj.get_sch_listener_killer_month()
                       ,day_of_week=config_obj.get_sch_listener_killer_day()
                       ,hour=config_obj.get_sch_listener_killer_hour()
                       ,minute=config_obj.get_sch_listener_killer_minute()
                       ,second=config_obj.get_sch_listener_killer_second())
   
    print('pulling from kafka ...')
    while True: 
        sys.stdout.flush()     
        json_stock_prediction =stock_pred.run(message, 0.5)# TODO: decide what todo with output
        time.sleep(5)
        
if __name__ == "__main__":
   main()
