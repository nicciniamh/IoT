#!/usr/bin/env python2
import sys, json
sys.path.append('lib')
import senclass

defs = json.loads(open('sensors.json').read())
sens = []
for s in defs:
    sen = senclass.instance(s["stype"], s["rtype"], s)
    sens.append({"name": s['Name'], 'sensor': sen})

for s in sens:
    print s['sensor'].getData(), '{} Data is {:.2f} seconds old'.format(s['name'],float(s['sensor'].age)),'\n'

print 'Done reading {} sensor(s)'.format(len(sens))

# ** Output like: ***

# __doc__ ' IoT sensor for temperature or humidity from DHT-like device. '
# __module__ 'dht'
# age 0.9307229518890381
# alarm ''
# disabled False
# drift 40.0
# high 100
# low 0
# maxAge 120
# senstype u'humidity'
# status 0
# stime 1504290352
# tstamp 1504290352.930723
# type 'dht'
# units '%'
# url u'http://rpi/sensor/temp'
# value 60.0
# Living Room (humidity) Data is 0.93 seconds old
# 
# __doc__ ' IoT sensor for temperature or humidity from DHT-like device. '
# __module__ 'dht'
# age 1.1818549633026123
# alarm ''
# disabled False
# drift 0
# high 100
# low 0
# maxAge 300
# senstype u'temperature'
# status 0
# stime 1504290352
# tstamp 1504290353.181855
# type 'dht'
# units u'c'
# url u'http://rpi/sensor/temp'
# value 19.0
# Living Room (temp) Data is 1.18 seconds old
# 
# __doc__ ' IoT sensor for temperature or humidity from DHT-like device. '
# __module__ 'dht'
# age -0.7341499328613281
# alarm ''
# disabled False
# drift u'v*0.95'
# high 100
# low -40
# maxAge 60
# senstype u'temperature'
# status 0
# stime 1504290354
# tstamp 1504290353.26585
# type 'dht'
# units u'f'
# url u'http://d1mini2.local/sensor/temp'
# value 69.35
# kitchen window Data is -0.73 seconds old
# 
# __doc__ ' IoT sensor for DS3232 RTC devices '
# __module__ 'ds3232'
# age 1.4630200862884521
# alarm ''
# disabled False
# drift 0
# high 100
# low -40
# maxAge 60
# senstype u'temperature'
# status 0
# stime 1504290352
# tstamp 1504290353.46302
# type 'ds3232'
# units u'f'
# url u'http://rpi3/sensor/temp'
# value 71.6
# ds3232 (temp) Data is 1.46 seconds old
# 
# Done reading 4 sensor(s)