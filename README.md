Internet of Things (IoT) Stuff

These files contain descriptions and exampls of my IoT Strategies. Please see 
[IoT Strategy.pdf](Iot%20Strategy.pdf)

I have three devices I use for my IoT

- [Banana Pi](http://www.bananapi.org/p/product.html) I use the M2 model
- [Raspberry Pi](https://www.raspberrypi.org/)  I am using a Pi model 2
- [WeMos D1 Mini](https://www.wemos.cc/product/d1-mini.html)

Both Pi units run Linux and the WeMos D1 uses 'bare-metal' code downloaded directly to the device. Each device has network connectivity. The Raspberry Pi uses Cat 5 Ethernet and the other devices use WiFi
```
The example code expects the following structure under home:
├── bin
│   └── dht.py           - Python Example
├── dhtlib               - Library for Python Example
│   ├── dhtpy.json       - JSON configuration for example code
    ├── iot.py           - iotSensor base class
    ├── dht.py           - dhtSensor class
│   ├── icons
│   │   ├── bpi.png
│   │   ├── dht.png
│   │   └── rpi.png
│   └── log.py
└── www                 - WWW Examples (I have this symlinked to my server folder)
    ├── dht11.php
    └── dht11x.php
```
