#!/usr/bin/python3

import urllib.request as ur
import threading 
import queue
import time

lock=threading.Lock()
pic_count=0

def downloader(q):
    global pic_count
    with lock:
        while not q.empty():
         try:
            ur.urlretrieve(q.get(block=False),"images{}image{}".format("/",pic_count))
            print("image{} downloaded".format(pic_count))
         except :
            print("image{} not downloaded".format(pic_count))
         q.task_done()
         pic_count+=1

q=queue.Queue()
with open("image_list.txt",'r') as f:
    for i in f.readlines():
        q.put(i[:-1])

start=time.time()
Thread_list=[]
for i in range(20):
    t=threading.Thread(target=downloader,args=[q])
    Thread_list.append(t)
    t.start()

q.join()


for i in Thread_list:
    i.join()
    print(i.name," has joined")

end=time.time()

print(end-start)
