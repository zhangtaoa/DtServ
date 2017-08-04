import multiprocessing
import time
import sys


a=10

def test(mydict):
    print("1111")
    print mydict
    print("1122")
    mydict["name1"]="ok"
    a=20
    return
    print("2222")



for i in range(1):
    mgr = multiprocessing.Manager()
    mydict=mgr.dict()
    mydict["name"]="test"
    print mydict
    print a
    p = multiprocessing.Process(target=test,args=(mydict,))
    #print(dir(p))
    p.daemon = True
    p.start()
    time.sleep(2)
    print p.is_alive()
    print("3333")
print a
print mydict
print mydict["name1"]
for key,value in mydict:
    print key,value
print("4444")
time.sleep(100)
