def find_oldest(path):
    fname_list=sorted(os.listdir(path))
    fname=fname_list[0]
    return fname 
    
    
class kafka_listener_thread (threading.Thread):
   def __init__(self, threadID, name, counter,configs):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.config_obj=configs# might be used in the future
  
   def schedul_kafka_listener(self):
       print("schedul_kafka_listener ")
       #to remove the previous twice old created folders containing models
       path=self.config_obj.get_main_path()+'/tempFolder'
       files=os.listdir(path)
       if(len(files)>2):#to keep at least 2 model
           oldest_path=path+'/' +find_oldest(path)
           shutil.rmtree(oldest_path, ignore_errors=False, onerror=None)
       time.sleep(5)
       #to run an independent process for listening to kafka. it will kills itself based on scheduler    
       proc=subprocess.Popen(["gnome-terminal", "--command=python /home/yasi/Documents/python_codes/child_kafka_puller.py"])

   def run(self):

       sched = Scheduler()
       sched.start()        # start the scheduler
#       #to test
       time_now=datetime.now()
#       sched.add_cron_job(self.schedul_kafka_listener, month='1-12', day_of_week=str(time_now.weekday()), hour='0-23', minute=time_now.minute, second=time_now.second+2)#after auto-trainer completely stored the new model
#       sched.add_cron_job(self.schedul_kafka_listener, month='1-12', day_of_week=str(time_now.weekday()), hour='0-23', minute=time_now.minute+20, second=4)#after auto-trainer completely stored the new model
       sched.add_cron_job(self.schedul_kafka_listener, year=2018,month=self.config_obj.get_sch_listener_month()
                   ,day_of_week=self.config_obj.get_sch_listener_day()
                   ,hour=self.config_obj.get_sch_listener_hour()
                   ,minute=self.config_obj.get_sch_listener_minute()
                   ,second=self.config_obj.get_sch_listener_second())

       
       while True:
           sys.stdout.flush()


      
class auto_trainer_thread (threading.Thread):
    def __init__(self, threadID, name, counter, configs):
        self.config_obj=configs
        threading.Thread.__init__(self)
        self.pre_time_auto_trainer=datetime.strptime(configs.get_news_start_datetime(),'%Y-%m-%d-%H-%M-%S')#make datetime
                    
    def schedul_auto_trainer(self):
        print("schedul_auto_trainer")
        curr_time=datetime.now()
        formatted_curr_time=datetime.strftime(curr_time, '%Y-%m-%d-%H-%M-%S')#make string
        formatted_pre_time=datetime.strftime(self.pre_time_auto_trainer, '%Y-%m-%d-%H-%M-%S')#make string
        command="--command=python /home/yasi/Documents/python_codes/child_model_trainer.py "+formatted_pre_time+" "+formatted_curr_time
        #to run an independent process for listening to kafka. it will kills itself based on scheduler    
        proc=subprocess.Popen(["gnome-terminal", command])
        self.pre_time_auto_trainer=curr_time

    
    def run(self):
        sched = Scheduler()  
        sched.start()
       # to test: need to be in .config
        time_now=datetime.now()
#        sched.add_cron_job(self.schedul_auto_trainer, month='1-12', day_of_week=str(time_now.weekday()), hour='0-23', minute=time_now.minute+4, second=time_now.second+4)
#        sched.add_cron_job(self.schedul_auto_trainer, month='1-12', day_of_week=str(time_now.weekday()), hour='0-23', minute=time_now.minute+30, second=4)
        sched.add_cron_job(self.schedul_auto_trainer, year=2018,month=self.config_obj.get_sch_trainer_month()
                           ,day_of_week=self.config_obj.get_sch_trainer_day()
                           ,hour=self.config_obj.get_sch_trainer_hour()
                           ,minute=self.config_obj.get_sch_trainer_minute()
                           ,second=self.config_obj.get_sch_trainer_second())

        while True:
            sys.stdout.flush()
       

def main():
    
    #to user enviroment variables , fill up myshell.sh

    try:
        config_obj=ConfigManager()
    except Exception:
        PrintException()
   
    threadLock = threading.Lock()

        
    threads = []

    thread1 = kafka_listener_thread(1, "Thread_kafka_listener", 1,config_obj)

    thread2 = auto_trainer_thread(2, "Thread_auto_trainer", 2, config_obj)

    thread1.start()# TODO: handle situation that no model exist in that path

    thread2.start()

    threads.append(thread1)

    threads.append(thread2)

    for t in threads:

        t.join()

            
    print "Exiting Main Thread"
    
    
    #Lock() method, which returns the new lock.
    #The acquire(blocking) method of the new lock object--> to force threads to run synchronously.
    # The optional blocking parameter enables you to control whether the thread waits to acquire the lock.
    # Start new Threads
    #blocking=1 --> thread returns immediately with a 0 value(if the lock cannot be acquired) or 1 value( if the lock was acquired)
    #blocking=0 --> the thread blocks --> wait for the lock to be released

if __name__ == "__main__":
#    rename_dir_files()
    main()
