import sys
sys.path.append('lib')
import senclass

defs = [{"tdrift": 0, "units": "f", "thigh": 100, "tlow": -40, "url": "http://rpi3/sensor/temp"},
        {"tdrift": 0, "units": "c", "thigh": 100, "tlow": 0, "url": "http://rpi/sensor/temp"},
        {"hdrift": 40, "units": "%", "hhigh": 100, "hlow": 0, "url": "http://rpi/sensor/temp"}
]
sens = [senclass.instance('ds3232', 'temperature',defs[0]),
        senclass.instance('dht',    'temperature',defs[1]),
        senclass.instance('dht',    'humidity',   defs[2])]

for s in sens:
    print s.getData(), 'Data is {0:.2f} seconds old'.format(float(s.age)),'\n'

# ** Output like: ***

# __doc__ ' IoT sensor for DS3232 RTC devices '
# __module__ 'ds3232'
# age 2.475977897644043
# alarm ''
# disabled False
# drift 0
# high 100
# low -40
# senstype 'temperature'
# status 0
# stime 1504252979
# tstamp 1504252981.475978
# type 'ds3232'
# units 'f'
# url 'http://rpi3/sensor/temp'
# value 71.6
# Data is 2.48 seconds old
# 
# __doc__ ' IoT sensor for temperature or humidity from DHT-like device. '
# __module__ 'dht'
# age 1.5043718814849854
# alarm ''
# disabled False
# drift 0
# high 100
# low 0
# senstype 'temperature'
# status 0
# stime 1504252980
# tstamp 1504252981.504372
# type 'dht'
# units 'c'
# url 'http://rpi/sensor/temp'
# value 19.0
# Data is 1.50 seconds old
# 
# __doc__ ' IoT sensor for temperature or humidity from DHT-like device. '
# __module__ 'dht'
# age 1.5851309299468994
# alarm ''
# disabled False
# drift 40.0
# high 100
# low 0
# senstype 'humidity'
# status 0
# stime 1504252980
# tstamp 1504252981.585131
# type 'dht'
# units '%'
# url 'http://rpi/sensor/temp'
# value 60.0
# Data is 1.59 seconds old
# 