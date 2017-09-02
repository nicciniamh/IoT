import json, inspect, urllib, time, sys, iot, urlData
from asteval import Interpreter
aeval = Interpreter()

class Sensor(iot.iotSensor):
    ''' IoT sensor for relay base class'''
    def __init__(self, d, sentype='relay'):
        ''' Constructor: paramter: dict with:
                         id = descriptive id
                         url = device url to read/write state
        '''
        self.disabled = False
        self.type = sentype
        self.url = d['url']

    def getData(self):
        ''' retrieve state from device. Provides for debounce 
            on slow devices with 500ms delay for up to 2.5 seconds. 
          '''
        if self.disabled:
            return self
        attempts = 5
        while attempts:
            try:
                self.status = 0
                self.tstamp = time.time()
                url = self.url
                data = urlData.getData(url)
                self.value = int(data['state'])
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

    def sendData(self,state):
        ''' Set relay state low or high (0/1) Provides for debounce 
            on slow devices with 500ms delay for up to 2.5 seconds. 
        '''
        if state:
            state = '1'
        else:
            state = '0'
        if self.disabled:
            return self
        attempts = 5
        while attempts:
            try:
                self.status = 0
                self.tstamp = time.time()
                url = '{}?state={}'.format(self.url,state)
                data = urlData.getData(url)
                self.value = int(data['state'])
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


    def maxAge(self,age):
        ''' set maximum data age '''
        self.maxAge = age
    
