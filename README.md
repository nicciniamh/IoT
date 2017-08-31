#Internet of Things (IoT) Stuff - Updated Version

These files contain descriptions and exampls of my IoT Strategies.

I have three devices I use for my IoT

- [Banana Pi](http://www.bananapi.org/p/product.html) I use the M2 model
- [Raspberry Pi](https://www.raspberrypi.org/)  I am using a Pi model 2
- [WeMos D1 Mini](https://www.wemos.cc/product/d1-mini.html)

Both Pi units run Linux and the WeMos D1 uses 'bare-metal' code downloaded directly to the device. Each device has network connectivity. The Raspberry Pi uses Cat 5 Ethernet and the other devices use WiFi

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

