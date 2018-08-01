# the created child process will kill itself
def schedul_kill():
    try:
        pid=os.getpid()
        os.kill(pid, signal.SIGTERM) # it kill both parent and child process
    except Exception:
        PrintException()

def main():
    try:
        input_param=sys.argv
#        print(input_param[1])
#        print(input_param[2])
        print("loading config file...")
        config_obj=ConfigManager()
        print('creating AutoTrainer object ...')
        auto_trainer = AutoTrainer(config_obj,input_param)
        auto_trainer.grabber_cleaner()# TODO: decide what todo with output
        time.sleep(5)
        auto_trainer.train_new_model()
        time.sleep(5)
        schedul_kill()
    except Exception:
        PrintException()    
        
if __name__ == "__main__":
   main()
