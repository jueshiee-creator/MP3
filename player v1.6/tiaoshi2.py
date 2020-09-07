import threading
import os
import time
 
def tt():
  info = threading.currentThread()
  while True:
    print ('pid: ', os.getpid())
    print (info.name, info.ident)
    time.sleep(3)
 
t1 = threading.Thread(target=tt)
t1.setName('OOOOOPPPPP')
t1.setDaemon(True)
t1.start()
 
t2 = threading.Thread(target=tt)
t2.setName('EEEEEEEEE')
t2.setDaemon(True)
t2.start()
 
 
t1.join()
t2.join()