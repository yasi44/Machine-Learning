"""
Created on Wed May 30 14:02:24 2018

@author: yasi
"""
from kafka import KafkaConsumer, KafkaProducer
import datetime as dt
from dateutil.tz import gettz
import re
import pytz
import json


def main():
#    #os.environ -> representing the string environment. they already have been set (os.environ["INPUT_TOPIC"]="abcd")
#    if 'INPUT_TOPIC' in os.environ:
#        input_topic = os.environ.get('INPUT_TOPIC')#will return one string
#    else:
#        print 'Missing INPUT_TOPIC in environment variables.'
#        sys.exit(0)
#    if 'GROUP_ID' in os.environ:
#        grp_id = os.environ.get('GROUP_ID')
#    else:
#        print 'Missing GROUP_ID in environment variables.'
#        sys.exit(0)
#    if 'BOOTSTRAP_SERVERS' in os.environ:
#        bootstrp_servers = os.environ.get('BOOTSTRAP_SERVERS')
#    else:
#        print 'Missing BOOTSTRAP_SERVERS in environment variables.'
#        sys.exit(0)
#    if 'OUTPUT_TOPIC' in os.environ:
#        output_topic = os.environ.get('OUTPUT_TOPIC')
#    else:
#        print 'Missing OUTPUT_TOPIC in environment variables.'
#        sys.exit(0) 
    consumer = KafkaConsumer('article',group_id='article',bootstrap_servers=bootstrp_servers,value_deserializer=lambda m: json.loads(m.decode('utf-8')),enable_auto_commit=False)
    if consumer:
        tz = pytz.timezone('Asia/Kuala_Lumpur')#py 2.7
        for msg in consumer:
            try:
                if 'content' and 'published_date' in msg:
                    date=msg['published_date']
                    content=msg['content']
                    if(re.search(u'[\u4e00-\u9fff]', content)):#ignore it if its chinese
                        pass
                    else:
                        file_name="kafka_grabbed_news/"+current_time+".txt"
                        news_file=open(file_name,"w")
                        news_file.write(msg)
                        print("news"+current_time+" has been written ")
                        news_file.close()
            except KeyError,e:
                print("ERR! no key for",e, "in id=", msg.key, "for json=",msg.value)
            except Exception, e:
                print(e,"Unexpected ERR occured for id=", msg.key, "for json=",msg.value)
            consumer.commit()
            
        
if __name__ == "__main__":
   main()
