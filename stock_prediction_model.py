# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 17:58:17 2018

@author: yasi
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 14:08:18 2018

@author: yasi
"""
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
import datetime as dt
import time
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

import string


def find_latest(path):
    fname_list=sorted(os.listdir(path))
    fname=fname_list[len(fname_list)-1]
    return fname 

class StockPrediction:
    def __init__(self):
        File=open("stockLabels2.labels","r")
        List=[""]
        for Line in File:
            List.append(string.replace(Line,'\n',''))
        self.labels=List
        result =False
        
        path=os.path.join('','savedMagpieModels')
        latest_path='savedMagpieModels/'+find_latest(path)
        self.model=Magpie(keras_model=str(latest_path+'/model.h5'), 
                  word2vec_model=str(latest_path+'/embedding'),
                  scaler=str(latest_path+'/scaler'),
                  labels=self.labels)
      def delete_model(self):
        del self.model
        
    def load_model(self):
        print('loading model ...')
        result =False
        path=os.path.join('','savedMagpieModels')
        try:#error handeling must be added 
            latest_path='savedMagpieModels/'+find_latest(path)
            self.model=Magpie(keras_model=str(latest_path+'/model.h5'), 
                  word2vec_model=str(latest_path+'/embedding'),
                  scaler=str(latest_path+'/scaler'),
                  labels=self.labels)
            print('2222')
            result=True
            print('model loaded')
        except:
            print('ERR in stockPrediction.loadModel()')
        return result
    

        
    def create_stocks_bool_json(self, magpie_result):        
        REstock=re.compile(r'[A-Z]+')
        REprobability=re.compile(r'[0][.][0-9]+')
        stock_names=[]
        stock_probability=[]
        for stock in magpie_result:
            magpie_result_str=str(stock)
            listToks=magpie_result_str.split(',')
            stock_names.append(listToks[0][2:-1])
            stock_probability.append(float(listToks[1][1:-1]))
                     
        #boolList=[0]*len(self.labels)
        json_dict = {}
        data = []
        for i in stock_names:
            temp_dic={}
            labelIndex=str(self.labels.index(i))
            if i== 'JCY':
                r=0
            if stock_probability[stock_names.index(i)] >self.THRESHOLD:
                temp_dic["name"]=i
                temp_dic["index"]=labelIndex
                temp_dic["prediction"]=1                         
            else:
                temp_dic["name"]=i
                temp_dic["index"]=labelIndex
                temp_dic["prediction"]=0                
            data.append(temp_dic)
        json_dict["news_number"]=100
        json_dict["prediction"]=data        
        return json_dict
            
            
    def run(self,news, threshold):
        self.THRESHOLD=threshold
        output=self.model.predict_from_text(news)
        return self.create_stocks_bool_json(output)
