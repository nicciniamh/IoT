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
        self.low = None
        self.high = None
        if senstype == 'temperature':
            if not 'units' in d:
                self.units = "f"
            else:
                if d["units"] == "c" or d["units"] == "f":
                    self.units = d["units"]
                else:
                    raise ValueError("Invalid units '{}' specified.".format(d["units"]))
            self.url = '{}?units={}'.format(d['url'],self.units)
            self.drift = float(d["tdrift"])
            self.high = d["thigh"]
            self.low = d["tlow"]
        else:
            self.high = d["hhigh"]
            self.low = d["hlow"]
            self.units = '%'
            self.url = d['url']
            self.drift = float(d["hdrift"])

        if self.low >= self.high:
            raise ValueError('temperature high cannot be less than temperature low')

        self.status = 0
        self.value = 0
        self.alarm = ''
        self.stime = 0.0
        
    def __str__(self):
        return "dhtSensor(type='{}' units={} id='({}){}' value={} status={} high={} low={} url='{}' alarm='{}'".format(self.sensType, self.units, self.sys,self.id, self.value, self.status, self.high, self.low, self.url,self.alarm)
    
    def setUnits(self,units):
        if self.sensType == "temperature":
            if units == "c" or units == "f":
                self.units = units
            else:
                raise ValueError("Invalid units '{}' specified.".format(units))
            self.url = '{}?units={}'.format(d['url'],self.units)
        return self
            
    def getData(self):
        ''' retrieve data from device raise dht_alarm on high or low value for temperature or hunidity '''

        data = json.loads(urllib.urlopen(self.url).read())
        
        self.tstamp = time.time()
        self.value = float(data[self.sensType]) + self.drift
        self.stime = int(data["time"])
        self.alarm = ''
        self.status = 0
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
    
