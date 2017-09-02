import os, time, sys, iot, urlData
from asteval import Interpreter

class Sensor(iot.iotSensor):
    ''' class for script execution '''
    def __init__(self, sdef):
        self.age = 0
        ''' Constructor: paramters: dict with variables for environment
                         script: python code for ateval to execute. Must return as part of overall loop
        '''
        self.stateData = {}

    def run(self, script,data):
        for k,v in self.stateData.items():
            data[k] = v
        data['stateData'] = self.stateData
        interpreter = Interpreter(data)
        interpreter.eval(script,0,True)
        for k,v in interpreter.symtable.items():
            if type(v) in [str,int,float,bool]:
                #print 'saving {} in stateData'.format(k)
                self.stateData[k] = v

        interpreter = None
