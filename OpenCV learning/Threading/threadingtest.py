import threading

def seks(threadname):
    for i in range(0,7):
        print("seks" + threadname+ '::' + str(i))
    
threads = []
t1 = threading.Thread(target=seks, args=('t1',))
t2 = threading.Thread(target=seks, args=('t2',))
t3 = threading.Thread(target=seks, args=('t3',))
t4 = threading.Thread(target=seks, args=('t4',))

threads.append(t1)
threads.append(t2)
threads.append(t3)
threads.append(t4)

#start threads
for t in threads:
    t.start()

#wait threads
for t in threads:
    t.join()

# make one thread processes

print (' FINAL SEKS')
