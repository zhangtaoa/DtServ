<%!
import sys
import requests
%><%
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
print inmsg
imsi = get_mml_value(inmsg,"IMSI")

reqmsg = """{"ROOT":{"BODY":{"OPR_INFO":{"LOGIN_NO":"aaa","OP_CODE":"1008","OP_NOTE":"xxx","LOGIN_ACCEPT":""},"BUSI_INFO":{"IMSI":"%s"}}}}""" % imsi.replace('"','')
indict["SReqMsg"] = reqmsg

url = "http://172.21.10.136:63000/esbWS/rest/com_sitech_ordersvc_person_atom_inter_s1007_IDynamicNumActiveAo_active"
headers = {'content-type': 'application/json; charset=utf-8'}

try:
   r = requests.post(url,data=reqmsg,headers=headers,timeout=30)
   if r.status_code == 200:
      indict["SRspMsg"] = r.text
      r_dict = r.json()
      return_code = r_dict["ROOT"]["BODY"]["RETURN_CODE"]
      return_msg = r_dict["ROOT"]["BODY"]["RETURN_MSG"]
      if return_code == "0":
         outmsg = "S0001:Operate success"
      else:
         outmsg = "E001:Operate failed"
   else:
      outmsg = "E001:Operate failed"
except:
   print sys.exc_info()
   outmsg = "E001:Operate failed"

%>${outmsg}