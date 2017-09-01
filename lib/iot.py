import inspect
''' base class for IoT sensors '''
class iotSensor:
    ''' Base class for IoT sensors - template class only ''' 
    def __init__(self):
        raise Exception('cannot instantiate base IoT sensor class')
    
    def sendData(self,data):
        ''' send data to IoT device '''
        return self
    def getData(self):
        ''' Retrieve data from IoT device '''
        return self
    
    def setHigh(self):
        ''' Set high limit for data '''
        return self
    
    def setLow(self):
        ''' Set low limit for data '''
        return self
    
    def isHigh(self):
        ''' Return boolean if data is equal or greater to high '''
        return false
    
    def isLow(self):
        ''' Return boolean if data is equal or less to low '''
        return false

    def __str__(self):
        ''' Show descriptive info about class '''
        x = ""
        for m,d in inspect.getmembers(self):
            o = ""
            if not inspect.ismethod(d) and not inspect.isfunction(d):
                o = '{} {}'.format(m,repr(d))
                x = '{} {}\n'.format(x,o)
        return x
    
class iotException(Exception):
    pass