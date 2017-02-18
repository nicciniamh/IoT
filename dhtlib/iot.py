#
# base class for IoT sensors
class iotSensor:
    ''' Base class for IoT sensors - template class only ''' 
    def __init__(self):
        raise Exception('cannot instantiate base IoT sensor class')
    
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
    
