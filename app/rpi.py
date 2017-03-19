import json
import time, threading
from app import app
import RPi.GPIO as GPIO

# GPIO ports on RPI for fingers
L_THUMB      = 19
L_INDEX      = 17
L_MIDDLE     = 27
L_RING       = 22
L_PINKY      = 5
L_PALM       = 6
L_BACK       = 13
R_THUMB      = 21
R_INDEX      = 23
R_MIDDLE     = 24
R_RING       = 25
R_PINKY      = 12
R_PALM       = 16
R_BACK       = 20

# timeout for check and also point of time
POINT_OF_TIME = 0.2

class RPI:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(L_THUMB, GPIO.OUT)
        GPIO.output(L_THUMB,False)
        GPIO.setup(L_INDEX, GPIO.OUT)
        GPIO.output(L_INDEX,False)
        GPIO.setup(L_MIDDLE, GPIO.OUT)
        GPIO.output(L_MIDDLE,False)
        GPIO.setup(L_RING, GPIO.OUT)
        GPIO.output(L_RING,False)
        GPIO.setup(L_PINKY, GPIO.OUT)
        GPIO.output(L_PINKY,False)
        GPIO.setup(L_PALM, GPIO.OUT)
        GPIO.output(L_PALM,False)
        GPIO.setup(L_BACK, GPIO.OUT)
        GPIO.output(L_BACK,False)
        GPIO.setup(R_THUMB, GPIO.OUT)
        GPIO.output(R_THUMB,False)
        GPIO.setup(R_INDEX, GPIO.OUT)
        GPIO.output(R_INDEX,False)
        GPIO.setup(R_MIDDLE, GPIO.OUT)
        GPIO.output(R_MIDDLE,False)
        GPIO.setup(R_RING, GPIO.OUT)
        GPIO.output(R_RING,False)
        GPIO.setup(R_PINKY, GPIO.OUT)
        GPIO.output(R_PINKY,False)
        GPIO.setup(R_PALM, GPIO.OUT)
        GPIO.output(R_PALM,False)
        GPIO.setup(R_BACK, GPIO.OUT)
        GPIO.output(R_BACK,False)
        self.gpio = {
            "L_THUMB":  L_THUMB,
            "L_INDEX":  L_INDEX,
            "L_MIDDLE": L_MIDDLE,
            "L_RING":   L_RING,
            "L_PINKY":  L_PINKY,
            "L_PALM":   L_PALM,
            "L_BACK":   L_BACK,
            "R_THUMB":  R_THUMB,
            "R_INDEX":  R_INDEX,
            "R_MIDDLE": R_MIDDLE,
            "R_RING":   R_RING,
            "R_PINKY":  R_PINKY,
            "R_PALM":   R_PALM,
            "R_BACK":   R_BACK
        }
        self.vms = {
            L_THUMB:  0,
            L_INDEX:  0,
            L_MIDDLE: 0,
            L_RING:   0,
            L_PINKY:  0,
            L_PALM:   0,
            L_BACK:   0,
            R_THUMB:  0,
            R_INDEX:  0,
            R_MIDDLE: 0,
            R_RING:   0,
            R_PINKY:  0,
            R_PALM:   0,
            R_BACK:   0
            }

    # we are running function every .2 seconds to check vibromotor status
    # we need to discount .2 seconds from finger timer if it is > 0
    # if timer is 0, we need to stop vibration
    def check_vibromotor(self):
        #print(time.ctime())
        #print(self.vms)
        for key,val in self.vms.items():
            v = int(val)
            #print("key=",key," val=",v)
            if v > 0:
                v = v-1
                if v == 0:
                    GPIO.output(key,False)    # switch off
                    print("GPIO.output(",key,",False)")
                self.vms[key] = str(v) # update
        self.ttt = threading.Timer(POINT_OF_TIME, self.check_vibromotor)
        self.ttt.start()
    # start vibration immediately and set timer when to stop it
    def start(self,finger,vstrength,vlen):
        # start vibration
        # we can't use strength in hardvare v1
        vst = vstrength
        vst = 0
        vl = 0
        if(vlen == 'undefined'):
            vl = 1
        else:
            vl = vlen
        GPIO.output(self.gpio[finger],True)    # switch on
        print("GPIO.output(",self.gpio[finger],",True)")
        # record timeout
        self.vms[self.gpio[finger]] = vl
    # stop vibration immediately and clear timeout
    def stop(self,finger):
        # stop vibration
        GPIO.output(self.gpio[finger],False)    # switch off
        print("GPIO.output(",self.gpio[finger],",False)")
        # clear timeot
        self.vms[self.gpio[finger]] = 0
    def __del__(self):
        self.ttt.cancel()

if __name__ == '__main__':
  app.run()
