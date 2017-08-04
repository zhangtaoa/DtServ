# DtServ
香港联通动态号码服务端

一、目前存在一个问题：
子进程退出后，父进程无法实时回收子进程，且关闭与客户端的socket连接，现在的实现方式如下：
#回收失效进程            
for key in ctrl_list:
print ctrl_dict
if ctrl_dict[key] == "close":
   print base_dict[key]
   print base_dict[key]["procss"]
   base_dict[key]["procss"].join()
   base_dict[key]["sockid"].close()
   ctrl_list.remove(key)
   base_dict.pop(key)

二、解决回收子进程的尝试办法有以下几种：
1、通过Queue ，在主进程实现调度的方式，伪代码如下

def 子进程：
    while True:
         接收请求
    mQdict["EVENT"]="CLOSE"

def Ioop(mQ):
    mQdict["EVENT"]="OPEN"
    sd,addr=accept()
    mQdict["SD"]=sd
    mQ.put(sd)

mQ=Queue()

#accpet进程
p=multiprocessing.Process(target=Ioop,args=(mQ))
p.daemon=True
p.start()

while True：
     myDict=mQ.get()
     if OPEN:
       创建子进程
     else CLOSE:
        关闭连接
        释放子进程
存在的问题：
对于socket、pprocess的对象QUEUE是不能支持传输的，只支持传输str和unicode。所有逻辑通，具体实现不了

2、定于全局变量进行控制
   存在的问题：子进程修改父进程的全局变量无效 ，所以行不通
   
 目前采用了代码中的实现方式，还望有大神提供解决方案
