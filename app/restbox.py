# work with restbox:
# 1. report to RESTbox controller own internal IP
# 2. ask it which finger vibration need to enable
import sys
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time, threading
from app import app

# timeout for check and also point of time (timeout in seconds to connect to restbox controller)
RESTBOX_POINT_OF_TIME = 3

class RESTbox:
    def __init__(self):
        # class variables
        self.host = '127.0.0.1'
        self.ip = os.environ['LMFEEDB_INT_IP']
        self.base_url = 'http://'+host+':80/api/gloves/lmfeedb/gloves1/'+self.ip
        self.proxies = {
            "http": None,
            "https": None,
        }
        self.headers = {'Content-Type':'application/json'}
    def check_controller(self):
        resp = requests.get(self.base_url, headers=self.headers, verify=False, proxies=self.proxies)
        print(resp)
        json_data = json.loads(resp.text)
        print(json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': ')))
        # install vibration on fingers
        self.ttt2 = threading.Timer(RESTBOX_POINT_OF_TIME, self.check_controller)
        self.ttt2.start()
    def __del__(self):
        self.ttt2.cancel()

if __name__ == '__main__':
  app.run()
