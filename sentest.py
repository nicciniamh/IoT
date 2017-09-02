#!/usr/bin/env python2
import sys, json, time
sys.path.append('lib')
import senclass
import script

sens = json.loads(open('sensors.json').read())
for s in sens:
    sen = senclass.instance(s["stype"], s)
    s["sensor"] = sen


for i in range(0,len(sens)):
    s = sens[i]
    print i, s['sensor'].getData(), '{} Data is {:.2f} seconds old'.format(s['Name'],float(s['sensor'].age)),'\n'

print 'Done reading {} sensor(s)'.format(len(sens))

scriptObjs = []

for s in sens:
    if s['stype'] == 'script':
        scr = s['sensor']
        scr.scriptText = open(s['script']).read()
        scriptObjs.append(scr)

if not len(scriptObjs):
    print 'No scripts to run, Exiting.'

print 'Looping {} script object(s)'.format(len(scriptObjs))
scriptData = {}
scriptData['time'] = time
for i in range(0,len(sens)):
    if sens[i]['stype'] == 'script':
        continue
    name = sens[i]['Name'].replace(' ','_').replace('(','_').replace(')','_')
    scriptData[name]= sens[i]['sensor']
    for k,v in sens[i].items():
        if k.lower() != 'name':
            k = '{}_{}'.format(name.replace(' ','_'),k)
            scriptData[k] = v
while True:
    for i in range(0,len(sens)):
        if sens[i]['stype'] != 'script':
            sens[i]['sensor'].getData()
    for scr in scriptObjs:
        scr.run(scr.scriptText,scriptData)
    time.sleep(10)
