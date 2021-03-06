import json, inspect, urllib, time, sys, iot, urlData, relaybaseclass
from asteval import Interpreter
aeval = Interpreter()

class Sensor(relaybaseclass.Sensor):
    ''' IoT sensor virtual relay'''
    def __init__(self, d, sentype='relay'):
        ''' Constructor: paramter: dict with:
                         id = descriptive id
                         url = device url to read/write state
        '''
        self.disabled = False
        self.type = 'virtualrelay'
        self.url = d['url']
        self.value = False
        if 'Name' in d:
            self.name = d['Name']
        else:
            self.name = 'virtual relay'

    def getData(self):
        self.age = 0
        return self

    def sendData(self,state):
        self.value = True if state else False
        self.age = 0
        print self.name,'set state to','on' if self.value else 'off'
        return self

    def maxAge(self,age):
        ''' set maximum data age '''
        self.maxAge = age
    
