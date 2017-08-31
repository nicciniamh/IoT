#
#
import json, inspect, urllib, time, sys, iot, urlData
from asteval import Interpreter
aeval = Interpreter()

class Sensor(iot.iotSensor):
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
        self.disabled = False
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
            self.drift = d["tdrift"]
            self.high = d["thigh"]
            self.low = d["tlow"]
        else:
            self.url = d['url']
            self.high = d["hhigh"]
            self.low = d["hlow"]
            if int(self.high + self.low) == 0:
                self.disabled = True
            else:
                self.disabled = False
                self.high = d["hhigh"]
                self.low = d["hlow"]
                self.units = '%'
                self.drift = float(d["hdrift"])

        if not self.disabled and self.low >= self.high:
            raise ValueError('temperature high cannot be less than temperature low')

        self.status = 0
        self.value = 0
        self.alarm = ''
        self.stime = 0
        
    def setUnits(self,units):
        if self.sensType == "temperature":
            if units == "c" or units == "f":
                self.units = units
            else:
                raise ValueError("Invalid units '{}' specified.".format(units))
            self.url = '{}?units={}'.format(d['url'],self.units)
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
                data = urlData.getData(self.url)
                self.tstamp = time.time()
                self.value = float(data[self.sensType])
                if type(self.drift) == int or type(self.drift) == float:
                    self.value = self.value + self.drift
                else:
                    aeval.symtable['v'] = self.value
                    self.value = aeval(self.drift)
                self.stime = int(data["time"])
                self.alarm = ''
                self.status = 0
                if self.value >= self.high:
                    self.alarm = 'High {} {}'.format(self.sensType,self.value)
                    self.status = 1
                elif self.value <= self.low:
                    self.alarm = 'Low {} {}'.format(self.sensType,self.value)
                    self.status = -1
                return self
            except urlData.dataException:
                self.alarm = 'No data ({})'.format(e)
            except TypeError as e:
                self.alarm = 'Invalid data ({})'.format(e)
            except ValueError as e:
                self.alarm = 'Decode error ({})'.format(e)
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
    
    def setHigh(self,high):
        self.high = high
        return self
    
    def setLow(self,low):
        self.low = low
        return self
    
if __name__ == "__main__":
    sys.path.append('.')
    d = {"tdrift": 0, "thigh": 100, "tlow": -40, "url": "http://rpi/sensor/temp"}
    dht = dhtSensor("temperature",d)
    dht.getData()
    print dht
