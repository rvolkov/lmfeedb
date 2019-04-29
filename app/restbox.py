# work with restbox:
# 1. report to RESTbox controller own internal IP
# 2. ask it which finger vibration need to enable
import sys
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time, threading
from app import rpi
from app import app

# timeout for check and also point of time (timeout in seconds to connect to restbox controller)
RESTBOX_POINT_OF_TIME = 3

class RESTbox:
    def __init__(self, RPI):
        # class variables
        self.host = 'ltrcrt2225.herokuapp.com'
        self.ip = os.environ['LMFEEDB_INT_IP']
        self.base_url = 'http://'+host+'/api/gloves/gloves1/lmfeedb4354/'+self.ip
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
        for gid, gstatus in json_data:
            self.tttlock.acquire()
            if gstatus = 1:
                self.RPI.start_api(gid)
            else:
                self.RPI.stop_api(gid)
            self.tttlock.release()
        # restart this function
        self.ttt2 = threading.Timer(RESTBOX_POINT_OF_TIME, self.check_controller)
        self.ttt2.start()
    def __del__(self):
        self.ttt2.cancel()

if __name__ == '__main__':
  app.run()
