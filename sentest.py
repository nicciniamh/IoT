import sys
sys.path.append('lib')
import senclass

defs = [{"tdrift": 0, "thigh": 100, "tlow": -40, "url": "http://rpi3/sensor/temp"},
        {"tdrift": 0, "thigh": 100, "tlow": -40, "url": "http://rpi/sensor/temp"}
]
sens = [senclass.instance('ds3232', 'temperature',defs[0]),
        senclass.instance('dht',    'temperature',defs[1])]

for s in sens:
    s.setUnits('c')
    print s.getData()
