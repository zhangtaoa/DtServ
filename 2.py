import requests

imsi="1234"

reqmsg = """{"ROOT":{"BODY":{"OPR_INFO":{"LOGIN_NO":"aaa","OP_CODE":"1008","OP_NOTE":"xxx","LOGIN_ACCEPT":""},"BUSI_INFO":{"IMSI":"%s"}}}}""" % imsi.replace('"','')


url = "http://172.21.10.136:63000/esbWS/rest/com_sitech_ordersvc_person_atom_inter_s1007_IDynamicNumActiveAo_active"
headers = {'content-type': 'application/json'}

r = requests.post(url,data=reqmsg,headers=headers)
print r.status_code
print r.json()