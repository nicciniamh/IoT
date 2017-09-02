import time, sys, urlData, relaybaseclass

class Sensor(relaybaseclass.Sensor):
    ''' IoT sensor virtual relay'''
    def __init__(self, d, sentype='relay'):
        ''' Constructor: paramter: dict with:
                         id = descriptive id
                         url = device url to read/write state
        '''
        self.disabled = False
        self.type = 'relay'
        self.url = d['url']
        self.value = False
        if 'Name' in d:
            self.name = d['Name']
        else:
            self.name = 'virtual relay'

    def getData(self):
        now = time.time()
        self.age = 0
        data = urlData.getData(self.url)
        self.value = data['state']
        return self

    def sendData(self,state):
        self.value = True if state else False
        self.age = 0
        cmd='on' if state else 'off'
        data = urlData.getData('{}?cmd={}'.format(self.url,cmd))
        self.value = data['state']
        return self

    