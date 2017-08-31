import json, inspect, urllib, time, sys, iot, urlData
from asteval import Interpreter
aeval = Interpreter()

class Sensor(iot.iotSensor):
    ''' IoT sensor for DS3232 RTC devices '''
    def __init__(self, senstype, d):
        ''' Constructor: paramters: type (always temperature)
                         d: dict with:
                             sys = system name
                             id = descriptive id
                             tdrift = float to add to temperature or humidty
                             thigh = float for high data value 
                             tlow  = float for low data value 
                             url = device url to obtain data
        '''
        if not senstype in ['temperature']:
            raise ValueError("Invalid sensor type {}".format(senstype))
        self.sensType = senstype;
        self.disabled = False
        self.low = None
        self.high = None
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

        if self.low >= self.high:
            raise ValueError('temperature high cannot be less than temperature low')

        self.status = 0
        self.value = 0
        self.alarm = ''
        self.stime = 0.0
        
    def setUnits(self,units):
        if self.sensType == "temperature":
            if units == "c" or units == "f":
                self.units = units
            else:
                raise ValueError("Invalid units '{}' specified.".format(units))
            self.url = '{}?units={}'.format(d['url'],self.units)
        return self
            
    def getData(self):
        ''' retrieve data from device set alarm on high or low
            value for temperature or hunidity. Provides for debounce 
            on slow devices with 500ms delay for up to 2.5 seconds. 
          '''
        attempts = 5
        while attempts:
            try:
                self.alarm = ''
                self.status = 0
                data = urlData.getData(self.url)
                self.tstamp = time.time()
                self.stime = int(data['time'])
                self.value = float(data[self.sensType])
                if type(self.drift) == int or type(self.drift) == float:
                    self.value = self.value + self.drift
                else:
                    aeval.symtable['v'] = self.value
                    self.value = aeval(self.drift)
                if self.value >= self.high:
                    self.alarm = 'High {} {}'.format(self.sensType,self.value)
                    self.status = 1
                elif self.value <= self.low:
                    self.alarm = 'Low {} {}'.format(self.sensType,self.value)
                    self.status = -1
                return self

            except urlData.dataException as e:
                self.value = 0.0
                self.status = 1
                self.alarm = 'No data ({})'.format(e)

            except TypeError as e:
                self.value = 0.0
                self.status = 1
                self.alarm = 'Invalid data ({})'.format(e)
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
    d = {"tdrift": 'int((v-32)*(5/9))', "thigh": 100, "tlow": -40, "url": "http://rpi3/sensor/temp"}
    ds = ds3232Sensor("temperature",d).setUnits('c')
    ds.getData()
    print ds
