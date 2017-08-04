#coding=utf-8
# Echo client program
import socket
import time

HOST = '172.21.10.136'    # The remote host
PORT = 12345              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
      print("Please input...")
      cmdstr = raw_input()
      print(cmdstr)
      print("1111")
      if cmdstr == "1":
         #登录
         s.send('CUHK-LOGIN:NAME="LOG1001",PASS="PAS1001";')
      elif cmdstr == "2":
         #开户
         s.send('CUHK-ADDACCOUNT:IMSI="454070000000000",ICCID="89860112349876543210",GT="85294931234";')
      elif cmdstr == "3":
         #心跳
         s.send('CUHK-CLIENTLIVE;')
      elif cmdstr == "4":
         #退出
         s.send('CUHK-LOGOUT;')

      data = s.recv(1024)
      print 'Received', repr(data)

time.sleep(500)