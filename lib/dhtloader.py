import sys
sys.path.append('.')
import dht
d = dht.dhtSensor('humidity',{"id":"dummy","url":"http://192.168.1.148/sensor/temp","hdrift":0, "hhigh":100, "hlow":10, "sys":"sys"})
print d.getData().value

