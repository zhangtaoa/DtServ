from multiprocessing import Process, Queue
import socket

def test(msg):
   print("msg")

def putMsg(q):
   mydict = {}
   print "i am put"
   mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
   print(mySocket)
   print(type(mySocket))
   ptest = Process(target=test,args=("i i",))
   mydict["pid"] = mySocket
   print mydict
   q.put(mydict)
   
def getMsg(q):
   print "i am get"
   print q.get()

if __name__=='__main__':
   q = Queue()
   p0 = Process(target=putMsg,args=(q,))
   p0.start()
   p1 = Process(target=getMsg,args=(q,))
   print(type(p1))
   if isinstance(type(p1),Process):
      print("111")
   
   p1.start()
   p0.join()
   p1.join()