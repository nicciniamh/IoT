# Internet of Things (IoT) Stuff - Updated Version

I have done a major revamp of the sensor class modules. Instead of being specific to sensor hardware they have classes of temperature, humidity, relay, etc. This is more in line the the IoT strategy of 
"abstraction" over the network. Unless there is a specific reason to use a specific sensor type it is better to use generic models. For example, I have two type of sensor devices but their internet servers 
serve the data in the same format, thus, there is no reson to differentiate between the two. 

----

These files contain descriptions and exampls of my IoT Strategies.


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

See [lib](lib/) for the specifics on the sensors.

