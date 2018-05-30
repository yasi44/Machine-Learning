# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 15:02:38 2018

@author: yasaman.eftekhary

purpose: connecting to the given links every 15 minutes and 
get the lates stock price data and store them in separate .csv file. 
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
import time
from dateutil.tz import gettz
import datetime


def scraping_BursaMalaysia(currentTime):
   fileName="StockPriceScrappedFromBursaMalaysia/"+currentTime+ ".txt"
   file=open(fileName,"w")
   link='http://www.bursamalaysia.com/market/securities/equities/prices/#/?filter=BS02'
   browser =webdriver.Chrome()#to initialize the browser object and go to a URL
   browser.get(link)

   
   el = browser.find_element_by_id('bursa_boards')
   for option in el.find_elements_by_tag_name('option'):
       if option.text == 'Main Market':
            option.click() # select() in earlier versions of webdriver
            break
   search_button = browser.find_element_by_id('bm_equity_price_search')
   search_button.click()
   time.sleep(10)
   innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
   soup=BeautifulSoup(innerHTML,"html.parser")
   soup.prettify()
   trs=soup.findAll('table')[0].findAll('tr')
   #trsContent=[]
   for trRow in trs:
       tds=trRow.findAll('td')
       tdTemp=[]
       for tdRow in tds:
           #print(tdRow)
           aTag=tdRow.find('a')
           if aTag:
               tdTemp.append(aTag.text)
           else:
               tdTemp.append(tdRow.text)
           #file.write("%s," % tdTemp)
       if tdTemp:
           for item in tdTemp:
               file.write("{};".format(item))
       file.write("\n")   
   file.close()
   
   #browser.close()        
   browser.quit()

   
def main():    
    #while True:
    # working hours of bursa malaysia: 9:00 AM - 12:30 PM, 2:30 PM to 5:00 PM
    tz = pytz.timezone('Asia/Kuala_Lumpur')#py 2.7
    now_utc = datetime.datetime.now(tz=tz)# py 2.7
    #now_utc = dt.datetime.now(dt.timezone.utc) # py3

    now = now_utc.astimezone(gettz('Asia/Kuala_Lumpur'))
    #now = dt.datetime.now()
    #currentTime= now.strftime("%Y_%m_%d_%H_%M_%S") #py 3
    currentTime=now_utc.isoformat()
    scraping_BursaMalaysia(currentTime)
#    weekDay=now.weekday()# Monday is 0 and Sunday is 6.
#    if (weekDay!=5 and weekDay !=6):
#        if((now.hour>=9 and now.hour<=11) and ( now.minute>=0 and now.minute<=59)) or \
#          (now.hour==12 and now.minute<=30) or \
#          (now.hour==14 and now.minute>=30) or \
#          ((now.hour>=15 and now.hour<=16) and ( now.minute>=0 and now.minute<=59)):
#              scraping_BursaMalaysia(currentTime)
    #time.sleep(650)
 
if __name__ == "__main__":
   main()
   print('end')

  
