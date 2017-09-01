import sys
sys.path.append('.')
import iot
import dht
import ds3232
'''
A nice little wrapper providing object reflection 
for the (currently) two defined sensor types. 
'''

def instance(stype, rtype, sendef):
    ''' -- IoT Sensor Interfacing
        instance() will instantiate a sensor of type stype with reading type and definitions dict
        parameters:
            stype: one of 'dht' or 'ds3232' (to add more add to imports in senclass.py)
            rtype: reading type for ds3232 its always temperature, dht temperature or humidity
            sendef: sensor specific definition dict, see the specific sensor class doc
    '''
    if not stype in globals():
        raise iot.iotException('No sensor of type {} defined.'.format(stype))
    return globals()[stype].Sensor(rtype,sendef)
