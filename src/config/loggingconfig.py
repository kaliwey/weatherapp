import sys
import os
import logging, logging.handlers
from config.config import config

# checks if logs path exists, if not we create it
if not os.path.exists(config.get('files','logs')):
    os.mkdir(config.get('files','logs'))
    
logs_path = config.get('files','logs')

fh = logging.handlers.RotatingFileHandler(logs_path+'/debug.log', maxBytes=1000000, backupCount=10)
fh.setLevel(logging.DEBUG)

fh2 = logging.handlers.RotatingFileHandler(logs_path+'/info.log', maxBytes=1000000, backupCount=5)
fh2.setLevel(logging.INFO)

er = logging.handlers.RotatingFileHandler(logs_path+'/errors.log', maxBytes=2000000, backupCount=2)
er.setLevel(logging.WARNING)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)

fh.setFormatter(logging.Formatter('%(asctime)s:%(threadName)s:%(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S"))
fh2.setFormatter(logging.Formatter('%(asctime)s:%(threadName)s:%(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S"))
er.setFormatter(logging.Formatter('%(asctime)s:%(threadName)s:%(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S"))
ch.setFormatter(logging.Formatter('%(asctime)s:%(threadName)s:%(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S"))


root = logging.getLogger()

#root.setLevel(logging.INFO)
#root.setLevel(logging.DEBUG)

root.setLevel(min([fh.level, fh2.level, ch.level, er.level]))

root.addHandler(fh)
root.addHandler(fh2)
root.addHandler(ch)
root.addHandler(er)