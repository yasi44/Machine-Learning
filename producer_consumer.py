# -*- coding: utf-8 -*-
"""
Created on Thu May  3 11:55:23 2018

@author: yasi
"""

# to develop a rest api that receive a news and return the a bool list of length 1260.
#each element shoes wherher that 

#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import os
from kafka import KafkaConsumer, KafkaProducer
import sys
import stockPredictionModel
import threading,logging, time
from stockPredictionModel import stockPrediction
from apscheduler.scheduler import Scheduler

sched = Scheduler()
sched.start()        # start the scheduler
stockPred = stockPrediction()
result=stockPred.loadModel()


def load_model():
    result=stockPred.loadModel()
    if(result==False):
        print('\n cannot load stockPred Model')


def main():
    #os.environ -> representing the string environment. they already have been set (os.environ["INPUT_TOPIC"]="abcd")
    if 'INPUT_TOPIC' in os.environ:
        input_topic = os.environ.get('INPUT_TOPIC')#will return one string
    else:
        print 'Missing INPUT_TOPIC in environment variables.'
        sys.exit(0)
    if 'GROUP_ID' in os.environ:
        grp_id = os.environ.get('GROUP_ID')
    else:
        print 'Missing GROUP_ID in environment variables.'
        sys.exit(0)
    if 'BOOTSTRAP_SERVERS' in os.environ:
        bootstrp_servers = os.environ.get('BOOTSTRAP_SERVERS')
    else:
        print 'Missing BOOTSTRAP_SERVERS in environment variables.'
        sys.exit(0)
    if 'OUTPUT_TOPIC' in os.environ:
        output_topic = os.environ.get('OUTPUT_TOPIC')
    else:
        print 'Missing OUTPUT_TOPIC in environment variables.'
        sys.exit(0)
     

    sched.add_cron_job(load_model, month='1-12', day_of_week='6', hour=22, minute=33)
    result=stockPred.loadModel()
    if(result==False):
        print('\n cannot load stockPred Model')
    else:
        #logging.basicConfig(format='', level= logging.INFO)
        consumer = KafkaConsumer(input_topic,group_id=grp_id,bootstrap_servers=bootstrp_servers,value_deserializer=lambda m: json.loads(m.decode('utf-8')),enable_auto_commit=False)	
        producer = KafkaProducer(bootstrap_servers=bootstrp_servers,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        stockPrediction = stockPredictionModel()
    
        print 'Broker:', bootstrp_servers
        print 'Consumer - Group_ID:', grp_id, 'Topic:', input_topic
        print 'Producer - Topic:', output_topic
        print 'Start polling...'
    
        for message in consumer:
            try:
                json_stockPrediction = stockPrediction.run(message.value, 0.5)# 0.5 is its threshold
                producer.send(output_topic,key=message.key, value=json_stockPrediction)		
            except KeyError,e:
                print "Error! No key for ", e, " in id=", message.key, "for json=", message.value
            except Exception, e:
                print e, " Unexpected error occur for id=", message.key, "for json=", message.value
            consumer.commit()

     
if __name__ == "__main__":
   main()

