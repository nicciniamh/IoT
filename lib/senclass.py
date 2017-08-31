import sys
sys.path.append('.')
import dht
import ds3232
''' A nice little wrapper to instantiate sensor of proper class based on stype. '''

def instance(stype, rtype, sendef):
    return globals()[stype].Sensor(rtype,sendef)
