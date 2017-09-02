import sys
import importlib
import iot
__loadedModules = {}
def __loadModule(module):
    ''' loadModule from module, store in the __loadedModules dictionary 
        parameters:
        module: module to load.
        Exceptions:
        iot.iotException when sensor class module not found.
    '''            
    if not module in __loadedModules:
        try:
            __loadedModules[module] = importlib.import_module(module,module)
        except Exception as e:
            raise iot.iotException('{}: {}'.format(module,e))

def instance(stype, sendef):
    '''
        Dynamic loading of IoT sensor module and sensor object instantiation.

        A nice little wrapper providing object reflection for sensor modules.

        instance() will instantiate a sensor of type stype with reading type and 
        definitions dict.

        parameters:
        stype: sensor class type
        rtype: reading type e.g., temperature, humidity
        sendef: sensor specific definition dict, see the specific sensor class doc
        Exceptions:
        iot.iotException when sensor class module not found.
    '''
    __loadModule(stype)
    return __loadedModules[stype].Sensor(sendef)
