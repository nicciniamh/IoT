# IoT and Sensors

## IoT
The IoT base class (iotSensor) does nothing and throws an exception when instantiated. 
The class is used simply as base for other IoT devices and allows for heterogenous 
device classes to be defined yet tested against the base class. 


Each IoT device at a minimum must provide a getData method to read the data or state of the 
device. 

The methods defined by the IoT base class are:
```
    sendData(data):  send data to IoT device, returns self
    getData() Retrieve data from IoT device, returns self
    setHigh() Set high limit for data, returns self
    setLow()  Set low limit for data, returns self
    isHigh()  Return boolean if data is equal or greater to high
    isLow()  Return boolean if data is equal or less to low
```

## *senclass* provides dynamic loading of IoT sensor module and sensor object instantiation.
This should be used when dynamic sensor typing is to be used by an application. Sensor class modules 
are not loaded until needed.

The instance function is used from senclass to instantiate a sensor. E.g.
``` sensor = senclass.instance('dht','temperature', {*definitiondict*}) ```
This will return sensor as a sensor with the same interfaces (as apporpriate) as IoT, overriding them where needed. 

## DHT
The dht.Sensor IoT class reads temperature or humidity from a DHT like sensor using urllib 
to get the data values in JSON format. 

The data expected has the format of: 
``` {"time":1487469162,"temperature":68,"units":"f","status":"ok","humidity":20} ```

The object is instantiated with:
 ```   dht = dht.Sensor(type, definition_dict) ```
Where
    type  is 'temperature' or 'humidity'
and
    definition dict has the following members:
                sys = system name
                id = descriptive id
                units = c or f for temperature sensors.
                [t|h]drift = float to add to temperature or humidty
                [t|h]high = float for high data value 
                [t|h]low  = float for low data value 
                url = device url from which to obtain data
'''
All of the iotSensor methods are available. Additional methods/properties are:
    setUnits(unts)  - set temperature units in c or f. 
    units   - c or f
    value   - current value since last getData call
    status  - status since last getData call (-1 low, 0 normal, 1 high)
    alarm   - current alarm text, blank if no alarm
    
Additionally the ```__str__``` method is defined so that str(dht.getValue()) or
str(dht) will return an ugly but full representation of the sensor's values and properties.

## DS3232
The ds3232.Sensor IoT class reads temperature from a ds3232 like sensor, using urllib 
to get the data values in JSON format. 

DS3232 realtime clock devices require a temperature sensor to ensure accuracy and they can be 
read on a Raspberry Pi via the I2C bus. 

The data expected has the format of: 
``` {"time":1487469162,"temperature":68,"units":"f","status":"ok"} ```

The object is instantiated with:
 ```   ds = ds3232.Sensor(type, definition_dict) ```
Where
    type  is always 'temperature'
and
    definition dict has the following members:
                sys = system name
                id = descriptive id
                units = c or f for temperature sensors.
                tdrift = float to add to temperature or humidty
                thigh = float for high data value 
                tlow  = float for low data value 
                url = device url from which to obtain data
'''
All of the iotSensor methods are available. Additional methods/properties are:
    setUnits(unts)  - set temperature units in c or f. 
    units   - c or f
    value   - current value since last getData call
    status  - status since last getData call (-1 low, 0 normal, 1 high)
    alarm   - current alarm text, blank if no alarm
    
Additionally the ```__str__``` method is defined so that str(dht.getValue()) or
str(dht) will return an ugly but full representation of the sensor's values and properties.


