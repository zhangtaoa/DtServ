from mako.template import Template

from mako.lookup import TemplateLookup
from mako.runtime import Context
from mako import exceptions
from StringIO import StringIO
import time
import os

lookup = TemplateLookup(directories=['/crmpdpp/sgwadm/work/zhangtaoa/mypy/DtServ'])

def serve_template(t_name, **kwargs):

    try:
       t = lookup.get_template(t_name)
       buf = StringIO()
       c = Context(buf, **kwargs)
       t.render_context(c)
       a = buf.getvalue()
       print "ss"
       print a
       print "ss1"
    except:
       print exceptions.text_error_template().render()
       
class MyTemplate():
   def __init__(self):
      self.lookDir = os.getcwd()
      print self.lookDir
      self.lookUp = TemplateLookup(directories=[self.lookDir])
      
   def GetLookUp(self):
      return self.lookUp
    
if __name__ == '__main__':
   name = {"name":"dingchunye"}
   #while True:
   #      serve_template("config/login.tpl.py",inmsg=name)
   #      time.sleep(3)           
   tt = MyTemplate().GetLookUp()
   ttt = tt.get_template("config/login.tpl.py")
   print ttt.render(inmsg=name)
