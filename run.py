#!/usr/local/bin/python3
import os
import socket
#os.environ['APP_ENV'] = 'production'
os.environ['APP_ENV'] = 'development'
from app import app
host = ''
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('www.cisco.com', 80))
    host = s.getsockname()[0]
    s.close()
except:
    host = '127.0.0.1'
os.environ['LMFEEDB_INT_IP'] = host
app.run(host=host,debug=True,port=5000)
#app.run(host='192.168.250.1',debug=True,port=80)
