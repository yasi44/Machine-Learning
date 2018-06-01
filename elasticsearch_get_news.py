
import json
import calendar
from elasticsearch import Elasticsearch
from datetime import datetime
import time
from apscheduler.scheduler import Scheduler
import sched
import sys

global_pre_time=int(datetime.strptime("01/01/2018", '%d/%m/%Y').strftime("%s"))#since we startted collecting from feb 2018

def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
       return False
    else:
       return True


def sche_get_from_elastic():
    curr_time=int(time.time())
    es = Elasticsearch()
    elasticsearch = '' ##### put the server ip
    es = Elasticsearch([elasticsearch])
    index = 'article'
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
    					"gte": global_pre_time,
    					"lte": curr_time,
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
    global global_pre_time
    global_pre_time=curr_time
    with open('news.json','w') as outfile:
        json.dump(res,outfile, encoding='utf-8')
        print("news.json has been created")
    
def main():
    curr_time=int(time.time())
    today= datetime.now().weekday()
    curr_min=datetime.now().minute
    curr_hour=datetime.now().hour
    sched = Scheduler()
    sched.start()        # start the scheduler
    
    #sched.add_cron_job(schedul_func, month='1-12', day_of_week=str((today+6)%7), hour=3, minute=15)
    #for test
    sched.add_cron_job(sche_get_from_elastic, month='1-12', day_of_week='0-6', hour='0-23', minute=curr_min+1, second=4)
    
    while True:
        sys.stdout.flush()     
        #json_stock_prediction =stock_pred.run(message, 0.5)
#        with open('json_stock_prediction.json','w') as outfile:
#            json.dump(json_stock_prediction,outfile, indent=4, sort_keys=True)
        time.sleep(5)
        
    
    
    
if __name__=="__main__":
    main()
