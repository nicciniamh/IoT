#!/usr/bin/env python2
import sys
sys.path.append('lib')
import senclass

defs = [{   
            "stype": "dht",
            "maxAge": 120,
            "rtype": "humidity",
            "hdrift": 40,
            "units": "%",
            "hhigh": 100,
            "hlow": 0,
            "url": "http://rpi/sensor/temp"
        },
        {   
            "stype": "dht",
            "rtype": "temperature",
            "tdrift": 0,
             "units": "c",
            "thigh": 100,
            "tlow": 0, 
            "url": "http://rpi/sensor/temp"
        },
        {
            "stype": "ds3232",
            "rtype": "temperature",
            "maxAge": 60,
            "tdrift": 0,
            "units": "f",
            "thigh": 100,
            "tlow": -40,
            "url": "http://rpi3/sensor/temp"
        }
]
sens = []
for s in defs:
    sen = senclass.instance(s["stype"], s["rtype"], s)
    sens.append(sen)

for s in sens:
    print s.getData(), 'Data is {0:.2f} seconds old'.format(float(s.age)),'\n'

# ** Output like: ***

# __doc__ ' IoT sensor for temperature or humidity from DHT-like device. '
# __module__ 'dht'
# age 1.046828031539917
# alarm ''
# disabled False
# drift 40.0
# high 100
# low 0
# maxAge 300
# senstype 'humidity'
# status 0
# stime 1504277509
# tstamp 1504277510.046828
# type 'dht'
# units '%'
# url 'http://rpi/sensor/temp'
# value 62.0
# Data is 1.05 seconds old
# 
# __doc__ ' IoT sensor for temperature or humidity from DHT-like device. '
# __module__ 'dht'
# age 1.1250760555267334
# alarm ''
# disabled False
# drift 0
# high 100
# low 0
# maxAge 300
# senstype 'temperature'
# status 0
# stime 1504277509
# tstamp 1504277510.125076
# type 'dht'
# units 'c'
# url 'http://rpi/sensor/temp'
# value 16.0
# Data is 1.13 seconds old
# 
# __doc__ ' IoT sensor for DS3232 RTC devices '
# __module__ 'ds3232'
# age 442.21956300735474
# alarm 'Stale data'
# disabled False
# drift 0
# high 100
# low -40
# maxAge 300
# senstype 'temperature'
# status 2
# stime 1504277068
# tstamp 1504277510.219563
# type 'ds3232'
# units 'f'
# url 'http://rpi3/sensor/temp'
# value 66.2
# Data is 442.22 seconds old
# 