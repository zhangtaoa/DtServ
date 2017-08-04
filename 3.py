import logging
import os

logDir=os.getcwd()
print logDir
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename=os.path.join(logDir,"logs/app.log"),
                filemode='a')
                
logger = logging.getLogger(__name__)

logger.info('Start reading database')
# read database here
 
records = {'john': 55, 'tom': 66}
logger.debug('Records: %s', records)
logger.info('Updating records ...')
# update records here
 
logger.info('Finish updating records')

 