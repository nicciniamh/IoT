import json, inspect, urllib, time, sys, iot, urlData
from asteval import Interpreter
aeval = Interpreter()

class Sensor(iot.iotSensor):
    ''' IoT sensor for temperature/humidity base class'''
    def __init__(self, d, sentype):
        ''' Constructor: paramter: dict with:
                         id = descriptive id
                         drift = float to add to temperature or humidty
                         high = float for high data value 
                         low  = float for low data value 
                         url = device url to obtain data
                         maxAge = number of seconds of age when data is considered stale
        '''
        self.disabled = False
        self.type = sentype
        self.low = None
        self.high = None
        self.url = d['url']
        if 'maxAge' in d:
            self.maxAge = int(d['maxAge'])
        else:
            self.maxAge = 300
        if self.type == 'temperature':
            if not 'units' in d:
                self.units = "f"
            else:
                if d["units"] == "c" or d["units"] == "f":
                    self.units = d["units"]
                else:
                    raise ValueError("Invalid units '{}' specified.".format(d["units"]))
        else:
            self.units = '%'
        self.drift = d["drift"]
        self.high = d["high"]
        self.low = d["low"]

        if self.low > self.high:
            raise ValueError('temperature high cannot be less than temperature low')

        self.status = 0
        self.value = 0
        self.alarm = ''
        self.stime = 0
        
    def setUnits(self,units):
        if self.type == 'temperature':
            if units == "c" or units == "f":
                self.units = units
            else:
                raise ValueError("Invalid units '{}' specified.".format(units))
        return self
            
    def getData(self):
        ''' retrieve data from device raise dht_alarm on high or low
            value for temperature or hunidity. Provides for debounce 
            on slow devices with 500ms delay for up to 2.5 seconds. 
          '''
        if self.disabled:
            return self
        attempts = 5
        while attempts:
            try:
                self.alarm = ''
                self.value = 0.0
                self.status = 1
                self.tstamp = time.time()
                url = '{}?units={}'.format(self.url,self.units)
                data = urlData.getData(url)
                self.value = float(data[self.type])
                if type(self.drift) == int or type(self.drift) == float:
                    self.value = self.value + self.drift
                else:
                    aeval.symtable['v'] = self.value
                    self.value = aeval(self.drift)
                self.stime = int(data["time"])
                self.alarm = ''
                self.status = 0
                if self.value >= self.high:
                    self.alarm = 'High {} {}'.format(self.type,self.value)
                    self.status = 1
                elif self.value <= self.low:
                    self.alarm = 'Low {} {}'.format(self.type,self.value)
                    self.status = -1
                self.age = self.tstamp - self.stime
                if self.age >= self.maxAge:
                    self.status = 2
                    self.alarm = 'Stale data'

                return self
            except urlData.dataException:
                self.alarm = 'No data ({})'.format(e)
            except TypeError as e:
                self.alarm = 'Invalid data ({})'.format(e)
            except ValueError as e:
                self.alarm = 'Decode error ({})'.format(e)
            self.age = self.tstamp - self.stime
            if self.age >= self.maxAge:
                self.status = 2
                self.alarm = 'Stale data'
            time.sleep(.5)
            attempts = attempts - 1
        return self            

    def getAlarm(self):
        if self.status == 0:
            return None
        return self.alarm

    def isHigh(self):
        return self.status == 1
    
    def isLow(self):
        return self.status == -1

    def isStale(self):
        return self.status == 2
    
    def setHigh(self,high):
        self.high = high
        return self
    
    def setLow(self,low):
        self.low = low
        return self

    def maxAge(self,age):
        self.maxAge = age
    
