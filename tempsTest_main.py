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
warnings.simplefilter("ignore")


new_process_flag=False
proc=0

def schedul_func():
    path=os.path.join('','savedMagpieModels')
    new_process_flag=True
    #subprocess.call('python /home/yasi/Documents/python\ codes/tempsTest.py', shell=True) 

    #this one works but opens a subprocess dependent to main process. we want a new independent process    
    proc=subprocess.Popen(["gnome-terminal", "--command=python /home/yasi/Documents/python\ codes/tempsTest.py"])
def main():
    
    new_process_flag=False
    File=open("stockLabels2.labels","r")
    List=[""]
    for Line in File:
        List.append(string.replace(Line,'\n',''))
        

    result =False
    path=os.path.join('','savedMagpieModels')
    #now = datetime.now()
    stock_pred = StockPrediction()
    labels=List    
    
    my_file=open('data2/noline3/2018-03-23-09-18-00.txt','r')
    message=my_file.read()
    
    sched = Scheduler()
    sched.start()        # start the scheduler
    
    sched.add_cron_job(schedul_func, month='1-12', day_of_week='1', hour='0-23', minute='0-59/2', second=10)
    #sched.add_cron_job(kill_process, month='1-12', day_of_week='1', hour=7, minute=36, second=45)
    

    schedul_func()
    print('main process started ...')
    while True:        
        sys.stdout.flush()
   
if __name__ == "__main__":
   main()
