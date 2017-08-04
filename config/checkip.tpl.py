<%
ips = ['172.21.10.131']
ip = inmsg[0]

if ip in ips:
   outmsg="1"
else:
   outmsg="0"

%>${outmsg}