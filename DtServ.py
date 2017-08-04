#coding=gbk

import sys
import os
import time
import socket
import multiprocessing
import logging
from multiprocessing import Queue
import json


from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions

info_dict={}
base_dict={}

class MyLog():
   def __init__(self):
      self.dd = time.strftime('%Y%m%d')
      self.logDir = os.getcwd()
      self.logname = "logs/serv_%s.log" % self.dd
      logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(process)d %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename=os.path.join(self.logDir,self.logname),
                filemode='a')
   
   def GetLogger(self):
      return logging.getLogger()

class MyTemplate():
   def __init__(self):
      self.lookDir = os.getcwd()
      print self.lookDir
      self.lookUp = TemplateLookup(directories=[self.lookDir])
      
   def GetLookUp(self):
      return self.lookUp
      
   def ExecTemplate(self, path, **inmsg):
      try:
         print path
         myTtt = self.lookUp.get_template(path)
         return myTtt.render(**inmsg)
      except:
         print exceptions.text_error_template().render()

class MyUtil():
   global info_dict
   def __init__(self):
      self.myTt = MyTemplate()

   def ParseMsg(self):
      msg = info_dict["CReqMsg"]
      if msg.startswith("CUHK-LOGIN"):
         msgType, msgValue = msg.split(":")
         return self.LogIn()
      elif msg.startswith("CUHK-LOGOUT"):
         return self.LogOut()
      elif msg.startswith("CUHK-CLIENTLIVE"):
         return self.ClientLive()
      elif msg.startswith("CUHK-ADDACCOUNT"):
         msgType, msgValue = msg.split(":")
         return self.AddAccount()
      else:
         return self.Default()
         
   def CheckIp(self,addr):
      return self.myTt.ExecTemplate("config/checkip.tpl.py",inmsg=addr)   
      
   def LogIn(self):
      return self.myTt.ExecTemplate("config/login.tpl.py",indict=info_dict)
      
   def LogOut(self):
      return self.myTt.ExecTemplate("config/logout.tpl.py")
      
   def ClientLive(self):
      return self.myTt.ExecTemplate("config/clientlive.tpl.py")
      
   def AddAccount(self):
      return self.myTt.ExecTemplate("config/addaccount.tpl.py",indict=info_dict)
      
   def Default(self):
      return self.myTt.ExecTemplate("config/default.tpl.py")



class MyTcp():
   global info_dict
   #global base_dict 
   def __init__(self,port):
       self.port = port
       self.ip = self.GetHostIp()
       self.mysocket = self.InitScoket()
       self.processnum = 0
      
   def GetHostIp(self):
       hostname = socket.gethostname()
       ip = socket.gethostbyname(hostname)
       
       return ip
       
   def InitScoket(self):
       mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
       mySocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
       #mySocket.settimeout(5)
       mySocket.bind((self.ip,self.port))
       mySocket.listen(10)
       
       return mySocket
   '''   
   def OpNum(self,optype):
       lock.acquire()
       if optype == "ADD":
          self.processnum = self.processnum+1
       elif optype == "MINUS":
          self.processnum = self.processnum+1
       lock.acquire()
   '''   
   def RecvReq(self, ctrl_dict, sd, addr):
       sd.settimeout(300) #防止telnet,33s未收到应答断开连接
       
       myUtil = MyUtil()
       
       if myUtil.CheckIp(addr) == "0":
          print str(sd)
          ctrl_dict[str(sd)] = "close"
          print ctrl_dict
          logmsg = "ip:[%s] is not allowd" % addr[0]
          mylog.info(logmsg)
          return
      
       self.processnum = self.processnum-1
        
       while True:
           print"aaa"
           try:
               print "bbb"
               reqMsg = sd.recv(1024)
               if len(reqMsg) == 0:
                  ctrl_dict[str(sd)] = "close"
                  return
               info_dict["CReqMsg"] = reqMsg
               print reqMsg
               
               rspMsg = myUtil.ParseMsg()
               sd.send(rspMsg)
               info_dict["CRspMsg"] = reqMsg
               logmsg = "CReqMsg:[%s]~SReqMsg:[%s]~SRspMsg:[%s]~CRspMsg:[%s]" % (info_dict.get("CReqMsg","") , info_dict.get("SReqMsg",""), info_dict.get("SRspMsg",""), info_dict.get("CRspMsg",""))
               mylog.info(logmsg)
               #登出特殊处理
               if reqMsg.startswith("CUHK-LOGOUT"):
                  self.processnum = self.processnum-1
                  ctrl_dict[str(sd)] = "close"
                  return 
           except Exception,e:
               print sys.exc_info()
               self.processnum = self.processnum-1
               ctrl_dict[str(sd)] = "close"
               return 
       
   def run(self):
       mgr = multiprocessing.Manager()
       ctrl_dict = mgr.dict()
       ctrl_list = []
       while True:
            tmp_dict = {}
            cliSd, cliAddr = self.mysocket.accept()
            p = multiprocessing.Process(target=self.RecvReq, args=(ctrl_dict, cliSd, cliAddr,))
            #ctrl_dict[str(cliSd)] = "open"
            tmp_dict["sockid"] = cliSd
            tmp_dict["cliaddr"] = cliAddr
            tmp_dict["procss"] = p
            base_dict[str(cliSd)] = tmp_dict
            ctrl_list.append(str(cliSd))
            p.daemon = True
            p.start()
            
            print ctrl_dict
            print type(ctrl_dict)
            print("bbbbbb")
            #回收失效进程
            for key in ctrl_list:
                print("aaaaaa")
                print ctrl_dict
                if ctrl_dict[key] == "close":
                   print("bbbbbb")
                   print base_dict[key]
                   print base_dict[key]["procss"]
                   base_dict[key]["procss"].join()
                   base_dict[key]["sockid"].close()
                   ctrl_list.remove(key)
                   base_dict.pop(key)

            
       #p.close()
       #p.join()
           

def Usage(errInfo):
   print(errInfo)
   sys.exit(1)

mylog = MyLog().GetLogger()

if __name__ == "__main__":

   if len(sys.argv) < 2:
      Usage("Correct Start Command : python %s port" % sys.argv[0])

   bindPort = int(sys.argv[1])
   if bindPort < 1024 or bindPort > 65535:
      Usage("You Input Port [%d] Invaild, Please Input [1024:65535]" % bindPort)

   tcpServ = MyTcp(bindPort)
   tcpServ.run()