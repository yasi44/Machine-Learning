# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 16:43:23 2018

@author: yasi

multithreading practice
"""
#!/usr/bin/python

import threading
import time
import os
import shutil


exitFlag = 0

def find_oldest(path):
    fname_list=sorted(os.listdir(path))
    fname=fname_list[0]
    return fname 
    
    
class kafka_listener_thread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
  
  def schedul_func():
    path=os.path.join('','tempFolder')
    #to remove the previous twice old created folders containing models
    oldest_path='tempFolder/'+find_oldest(path)
    shutil.rmtree(oldest_path, ignore_errors=False, onerror=None)
    time.sleep(5)
    #to run an independent process for listening to kafka. it will kills itself based on scheduler    
    proc=subprocess.Popen(["gnome-terminal", "--command=python /home/yasi/Documents/python\ codes/child_kafka_puller.py"])

   def run(self):
#      print "Starting " + self.name
#      threadLock.acquire() # Get lock to synchronize threads
#      print_time(self.name, 5, self.counter)
#      threadLock.release() # Free lock to release next thread
#      print "Exiting " + self.name
       stock_pred = StockPrediction()       
       # to test instead of kafka news
       my_file=open('data2/noline3/2018-03-23-09-18-00.txt','r')
       message=my_file.read()
       sched = Scheduler()
       sched.start()        # start the scheduler
       today= datetime.now().weekday()
       curr_min=datetime.now().minute
       curr_hour=datetime.now().hour
       sched.add_cron_job(schedul_func, month='1-12', day_of_week=str(today), hour='0-23', minute='0-59/2', second=4)
       schedul_func()
       print('main process started ...')
       while True:
           sys.stdout.flush()

def print_time(threadName, counter, delay):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print "%s: %s" % (threadName, time.ctime(time.time()))
      counter -= 1
      
class auto_trainer_thread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
#      print "Starting " + self.name
#      threadLock.acquire() # Get lock to synchronize threads
#      print_time(self.name, 5, self.counter)
#      threadLock.release() # Free lock to release next thread
#      print "Exiting " + self.name
       TODO: need to be completed

def print_time(threadName, counter, delay):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print "%s: %s" % (threadName, time.ctime(time.time()))
      counter -= 1

threadLock = threading.Lock()
threads = []

# Create new threads
thread1 = kafka_listener_thread(1, "Thread_kafka_listener", 1)
thread2 = auto_trainer_thread(2, "Thread_auto_trainer", 2)

# Start new Threads
thread1.start()# TODO: handle situation that no model exist in that path
thread2.start()



# Add threads to thread list
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"


#Lock() method, which returns the new lock.
#The acquire(blocking) method of the new lock object--> to force threads to run synchronously.
# The optional blocking parameter enables you to control whether the thread waits to acquire the lock.
# Start new Threads
#blocking=1 --> thread returns immediately with a 0 value(if the lock cannot be acquired) or 1 value( if the lock was acquired)
#blocking=0 --> the thread blocks --> wait for the lock to be released
