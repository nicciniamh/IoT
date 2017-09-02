import json, inspect, urllib, time, sys, iot, urlData, thbaseclass
from asteval import Interpreter
aeval = Interpreter()

class Sensor(thbaseclass.Sensor):
    ''' IoT sensor for humidity '''
    def __init__(self, d):
        ''' Constructor: paramters: dict with:
                         id = descriptive id
                         drift = float to add to temperature or humidty
                         high = float for high data value 
                         low  = float for low data value 
                         url = device url to obtain data
                         maxAge = number of seconds of age when data is considered stale
        '''
        thbaseclass.Sensor.__init__(self,d,'humidity')
