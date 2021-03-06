# work with restbox:
# 1. report to RESTbox controller own internal IP
# 2. ask it which finger vibration need to enable
import sys
import os
import json
import requests
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time, threading
from app import rpi
from app import app

# timeout for check and also point of time (timeout in seconds to connect to restbox controller)
RESTBOX_POINT_OF_TIME = 3

class RESTbox:
    def __init__(self, RPI):
        # class variables
        self.host = os.environ['LMFEEDB_CONTROLLER_HOST']
        self.ip = os.environ.get('LMFEEDB_INT_IP','0.0.0.0')
        self.passphrase = os.environ['LMFEEDB_CONTROLLER_PASS']
        self.base_url = 'http://'+self.host+'/api/gloves/gloves1/'+self.passphrase+'/'+self.ip
        self.proxies = {
            "http": None,
            "https": None,
        }
        self.headers = {'Content-Type':'application/json'}
        self.tttlock = threading.Lock()
        self.RPI = RPI
        #self.RPI = rpi.RPI()
        #self.RPI.init_check()
        #self.RPI.check_vibromotor()  # start thread
    def check_controller(self):
        resp = requests.get(self.base_url, headers=self.headers, verify=False, proxies=self.proxies)
        print(resp)
        json_data = json.loads(resp.text)
        print(json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': ')))
        # install vibration on fingers
        for ggg in json_data["message"]:
            #print("ggg=",ggg)
            #print("ggg.status=",ggg["status"])
            #print("ggg.id=",ggg["id"])
            #for gid, gstatus in json_data["message"]:
            self.tttlock.acquire()
            iddd = int(ggg["id"])
            #print("iddd=",iddd)
            if ggg["status"] == 1:
                self.RPI.start_api(iddd)
            else:
                self.RPI.stop_api(iddd)
            self.tttlock.release()
        # restart this function
        self.ttt2 = threading.Timer(RESTBOX_POINT_OF_TIME, self.check_controller)
        self.ttt2.start()
    def __del__(self):
        self.ttt2.cancel()

if __name__ == '__main__':
  app.run()
