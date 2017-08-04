<%
def get_mml_value(msg, key):
    if len(msg) == 0 or len(key) == 0:
       return None

    start_pos = msg.find(key)
    end_pos = msg.find(",",start_pos)
    if end_pos < 0:
       end_pos = msg.find(";",start_pos)

    value=msg[start_pos+len(key)+1:end_pos]
    return value

inmsg = indict["CReqMsg"]
name = get_mml_value(inmsg,"NAME")
passwd = get_mml_value(inmsg,"PASS")

outmsg = "S0001:Operate success"

if name.replace('"','') != "LOG1001":
   outmsg = "E001:Operate failed"
   
if passwd.replace('"','') != "PAS1001":
   outmsg = "E001:Operate failed"

%>${outmsg}