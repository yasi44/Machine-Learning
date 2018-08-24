
import re
import json
import shutil
import os
from bs4 import *
import time
from magpie import Magpie
from elasticsearch import Elasticsearch
import string
import datetime
from datetime import datetime
import mysql.connector as msc #for py2.7
from datetime import timedelta
from text_clean import clean
from exception_handling import PrintException
from mysql_connector import MYSQLConnector
from collections import defaultdict
from config_manager import ConfigManager
from stock_prediction_model import StockPrediction
import codecs

import gzip
import StringIO

import matplotlib
from numpy.random import randn
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter 


#for post request
from flask import Flask, abort, request 
import json
import numpy as np

KL_holidays=['2018-01-01', '2018-01-31',
          '2018-02-01', '2018-02-16', '2018-02-17',
          '2018-05-01', '2018-05-09', '2018-05-10','2018-05-11','2018-05-29','2018-05-30','2018-05-31',
          '2018-06-02', '2018-06-15', '2018-06-16',
          '2018-08-22', '2018-08-31', 
          '2018-09-09', '2018-09-11', '2018-09-16',
          '2018-11-06', '2018-11-20', 
          '2018-12-25']

config_obj=ConfigManager()
stock_pred = StockPrediction()
with open("res_result.json") as f:
        res=json.load(f)
start_date= datetime(2018, 8, 1, 0, 0, 0)
start_date_int=int(start_date.strftime("%s"))*1000
end_date=datetime(2018, 8, 15, 0, 0, 0)
end_date_int=int(end_date.strftime("%s"))*1000
stk='CIMB'        
  
  

      
def draw_plot(res,start_date_in, end_date_in,stk):
    try:
        start_date_local=start_date_in
        date_info_date=[]
        date_info_num_news=[]
        date_info_num_positive_news=[]
        date_info_percent=[]
        one_day = timedelta(days=1)
        
        news_date=[]
        total_news=[]
        pos_news=[]
        try:
            while(start_date_local<= end_date_in):
                if(np.is_busday(start_date_local,holidays=KL_holidays)):
                    news_date.append(start_date_local)
                    total_news.append(0)
                    pos_news.append(0)
                start_date_local = start_date_local + one_day

            for doc in res['hits']['hits']:            
                doc_date=doc['_source']['published_date']
                doc_date_refined=doc_date[:doc_date.find('+')]
                doc_date_refined=doc_date_refined.replace('T','-')
                doc_date_refined=doc_date_refined.replace(':','-')
                doc_date_refined=datetime.strptime(doc_date_refined, '%Y-%m-%d-%H-%M-%S')#convert to datetime
                doc_date_refined=doc_date_refined.replace(hour=0, minute=0, second=0)                
                if(doc_date_refined in news_date):
                    if(np.is_busday(doc_date_refined,holidays=KL_holidays)):# need to be changed, if news of pubic holidays are also required to be considered
                        total_news[news_date.index(doc_date_refined)] +=1
                        doc_content=doc['_source']['content']
                        doc_content=doc_content.encode('ascii', 'ignore')# limits news to english only
                        cleaned_news=clean(news_str=doc_content,configs=config_obj)#writes in 'elastic_grabbed_news' folder
                        cleaned_news=cleaned_news.encode('ascii', 'ignore')
                        json_stock_prediction =stock_pred.run(cleaned_news, 0.5)# TODO: decide what todo with output
                        if(json_stock_prediction['prediction'][stk]['prediction']==1):
                            pos_news[news_date.index(doc_date_refined)] +=1
            
            percentage=[]
            counter=0
            while(counter<len(news_date)):
                if total_news[counter]!=0:
                    percentage.append(float(pos_news[counter])/float(total_news[counter]))
                else:
                    percentage.append(0.0)
                counter += 1
                

            dates = matplotlib.dates.date2num(news_date)
            ee=dict(zip(dates, percentage))
        except Exception as e:
           PrintException(e, exitStatus=True)
  
        return ee
        

    except:
        return 0


app = Flask(__name__)


@app.route('/foo', methods=['POST']) 
def foo():
    if not request.json:
        abort(400)
    print "hi"
    result=json.dumps(draw_plot(res,start_date,end_date,stk))

    
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True,use_reloader=False)
