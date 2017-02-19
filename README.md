#Internet of Things (IoT) Stuff - Updated Version

These files contain descriptions and exampls of my IoT Strategies.

I have three devices I use for my IoT

- [Banana Pi](http://www.bananapi.org/p/product.html) I use the M2 model
- [Raspberry Pi](https://www.raspberrypi.org/)  I am using a Pi model 2
- [WeMos D1 Mini](https://www.wemos.cc/product/d1-mini.html)

Both Pi units run Linux and the WeMos D1 uses 'bare-metal' code downloaded directly to the device. Each device has network connectivity. The Raspberry Pi uses Cat 5 Ethernet and the other devices use WiFi

The example code expects the following structure:
dhtx.py             Python/tkinter multi-threaded example program
lib/                Class Libraries
lib/iot.py          iotSensor Base Class
lib/dht.py          dhtSensor class
lib/dhtpy.json      JSON format configuration
lib/icons           Icons
lib/icons/bpi.png   BananaPi logo, 32x32
lib/icons/dht.png   DHT11 logo, 32x32
lib/icons/rpi.png   RaspberryPi logo, 32x32

#IoT and DHT

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
## DHT
The dhtSensor IoT class reads temperature or humidity from a DHT like sensor using urllib 
to get the data values in JSON format. 

The data expected has the format of: 
``` {"time":1487469162,"temperature":68,"units":"f","status":"ok","humidity":20} ```

The object is instantiated with:
 ```   dht = dhtSensor(type, definition_dict) ```
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
str(dht) will return an ugly but fill representation of the sensor's values and properties.

