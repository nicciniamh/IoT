import sys
sys.path.append('.')
import dht
import ds3232
''' A nice little wrapper providing object reflection for the (currently) two defined sensor types. '''

def instance(stype, rtype, sendef):
    return globals()[stype].Sensor(rtype,sendef)
