#!/usr/bin/env python2
import sys, json
sys.path.append('lib')
import senclass

defs = json.loads(open('sensors.json').read())
sens = []
for s in defs:
    sen = senclass.instance(s["stype"], s)
    sens.append({"name": s['Name'], 'sensor': sen})

for s in sens:
    print s['sensor'].getData(), '{} Data is {:.2f} seconds old'.format(s['name'],float(s['sensor'].age)),'\n'

print 'Done reading {} sensor(s)'.format(len(sens))

