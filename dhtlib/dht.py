#
#
import json 
import urllib
import time
import sys
import iot

class dhtSensor(iot.iotSensor):
    ''' temperature / humidity IoT sensor. Read dht data from url. '''
    def __init__(self, senstype, d):
        ''' Constructor: paramters: type [temperature|humidity]
                         d: dict with:
                         sys = system name
                         id = descriptive id
                         [t|h]drift = float to add to temperature or humidty
                         [t|h]high = float for high data value 
                         [t|h]low  = float for low data value 
                         url = device url to obtain data
        '''
        if not senstype in ['temperature','humidity']:
            raise ValueError("Invalid sensor type {}".format(senstype))
        
        self.sensType = senstype;
        self.sys = d["sys"]
        self.id = d["id"]
        self.url = d['url']
        if senstype == 'temperature':
            self.drift = float(d["tdrift"])
            self.high = d["thigh"]
            self.low = d["tlow"]
        else:
            self.drift = float(d["hdrift"])
            self.high = d["hhigh"]
            self.low = d["hlow"]

        if self.low >= self.high:
            raise ValueError('temperature high cannot be less than temperature low')

        self.status = 0
        self.value = 0
        self.alarm = ''
        
    def __str__(self):
        return "dhtSensor(type='{}' id='({}){}' value={} status={} high={} low={} url='{}' alarm='{}'".format(self.sensType, self.sys,self.id, self.value, self.status, self.high, self.low, self.url,self.alarm)
    
    def getData(self):
        ''' retrieve data from device raise dht_alarm on high or low value for temperature or hunidity '''

        data = json.loads(urllib.urlopen(self.url).read())
        
        self.tstamp = time.time()
        self.value = float(data[self.sensType]) + self.drift
        self.stime = int(data["time"])
        if self.value >= self.high:
            self.alarm = 'High {}'.format(self.sensType)
            self.status = 1
        elif self.value <= self.low:
            self.alarm = 'Low {}'.format(self.sensType)
            self.status = -1
        return self

    def isHigh(self):
        return self.status == 1
    
    def isLow(self):
        return self.status == -1
    
    def setHigh(self,high):
        self.high = high
        return self
    
    def setLow(self,low):
        self.low = low
        return self
