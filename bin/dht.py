#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

#
# read and display in a nice little tkInter gui temperature/humidity data based on a config file in JSON format.
#
logtext = "";
import os, sys, json, urllib, threading, time
from Tkinter import *

home = os.path.expanduser("~")
sys.path.append(home+"/dhtlib");

from log import logger

config = home+"/dhtlib/dhtpy.json"
print "Using config in",config



try:
    conf = json.loads(open(config).read())
    icondir = conf["icondir"].replace("$home",home)
    repmap =  { "$icondir": icondir, "$home": home }

    for k,v in conf.iteritems():
        if isinstance(v,basestring):
            for a,b in repmap.iteritems():
                conf[k] = v.replace(a,b)

                
except Exception as e:
    print >>sys.stderr, "Cannot read config ",config, str(e)
    sys.exit(1)


appicon = conf["appicon"]

degree_sign= u'\N{DEGREE SIGN}'


log = logger()

class dhtItem:
    """ 
    class for dhtItems to initialize things properly from the 
    configuration dict, set up the labes for display and collect data/ 
    """
    def __init__(self, master, dh):
        self.sys = dh["sys"]
        self.id = dh["id"]
        log.message("Created "+self.id+"("+self.sys+")");
        self.url = conf["baseurl"].replace('$sys',self.sys);
        self.tdrift = float(dh["tdrift"])
        self.hdrift = float(dh["hdrift"])
        self.thigh = dh["thigh"]
        self.tlow = dh["tlow"]
        self.hhigh = dh["hhigh"]
        self.hlow = dh["hlow"]
        self.logo = dh["logo"].replace("$icondir",icondir)
        self.logo = PhotoImage(file=self.logo)
        self.image = Label(master,image=self.logo)
        self.temp = None
        self.humidity = None
        self.idlabel = Label(master,text=self.id+"("+self.sys+")", justify=LEFT)
        self.idlabel.config(font=int(conf["fsize"]))
        self.tlabel = Label(master, text="", justify=RIGHT)
        self.tlabel.config(font=int(conf["fsize"]))
        self.hlabel = Label(master, text="", justify=RIGHT)
        self.hlabel.config(font=int(conf["fsize"]))
        self.tmlabel = Label(master, text="", justify=RIGHT);
        self.tmlabel.config(font=int(conf["fsize"]))
        
    #
    # Here we do our data collection by reading JSON data from the 
    # url in conf[] and the the sys property of dhtItem and 
    # attempt to handle errors. 
    #
    def getData(self):
        try:
            data = json.loads(urllib.urlopen(self.url).read())
            
            self.temp = float(data["tf"]) + self.tdrift
            self.humidity  = int(float(data["h"])  + self.hdrift)
            self.stime = int(data["time"])
            tcolor = "green2"
            if self.temp >= self.thigh:
                tcolor = "red"
            if self.temp <= self.tlow:
                tcolor = "blue"

            hcolor = "green2"
            if self.humidity >= self.hhigh:
                hcolor = "red"
            if self.humidity <= self.hlow:
                hcolor = "blue"
            tstr = str(self.temp)+degree_sign+'F'
            hstr = str(self.humidity)+'%'

        except Exception, e:
            log.message("Cannot get data for "+sys+": "+str(e)+"\n");
            tstr = str(e)
            tcolor = "red"
            
        self.tlabel.config(text=tstr, fg=tcolor)
        self.hlabel.config(text=hstr, fg=hcolor)
        self.tmlabel.config(text=str(time.strftime('%x %X', time.localtime(self.stime))))

#
# This is our main class
#
class DHT:
    def __init__(self, master):
        self.master = master;
        master.title(conf["title"])
        log.message(conf["title"]+": startup");
        self.dhtItems = [];
        self.label = Label(master, text="DHT11 Monitors")
        self.label.grid(row=0,column=0)
        self.label.config(font=int(conf["fsize"]))
        
        for i in range(len(conf["dhts"])):
            dht = conf["dhts"][i]
            d = dhtItem(master,dht)
            d.idlabel.grid(row=i,column=0)
            d.image.grid(row=i,column=1)
            d.tlabel.grid(row=i,column=2)
            d.hlabel.grid(row=i,column=3)
            d.tmlabel.grid(row=i,column=4)
            self.dhtItems.append(d)
            
        self.isQuit = False;
        self.close = Button(master, text="Close", command=self.stop).grid(row=len(self.dhtItems)+2,column=4)
        threading.Timer(1.0,self.collectData).start()
    
    def stop(self):
        log.message("stop requested.")
        self.isQuit = True
        
    def collectData(self):
        for d in self.dhtItems:
            try:
                d.getData()
            except Exception as e:
                log.message(d.sys+": collect data error: "+e) 
                print str(e)
        if self.isQuit:
            self.master.quit()
            log.message("Exiting - Showing last up to last 10 lines of log.");
            print log.tail(12)
            sys.exit(1)
        else:
            threading.Timer(1.0,self.collectData).start()
                
root = Tk()
img = Image("photo", file=appicon)
root.tk.call('wm','iconphoto',root._w,img)

my_gui = DHT(root)
try:
    root.mainloop()
except KeyboardInterrupt:
    print "KeyboardInterrupt"
    my_gui.stop()
