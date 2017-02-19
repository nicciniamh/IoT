#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

#
# read and display in a nice little tkInter gui temperature/humidity data based on a config file in JSON format.
#
import os, sys, json, urllib, threading, time, logging, Queue
from Tkinter import *

sys.path.append("./lib");
import iot
import dht

config = "lib/dhtpy.json"
print "Using config in",config


try:
    conf = json.loads(open(config).read())
                
except Exception as e:
    print >>sys.stderr, "Cannot read config ",config, str(e)
    sys.exit(1)


appicon = conf["appicon"]
degree_sign= u'\N{DEGREE SIGN}'

if not "labelcolors" in conf:
	colors = ["blue2","green2","red"]
else:
	colors = conf["labelcolors"]

if not 'bgcolor' in conf:
	bgcolor = "black"
else:
	bgcolor = conf["bgcolor"]
	
if not 'fgcolor' in conf:
	fgcolor = "white"
else:
	bgcolor = conf["fgcolor"]

class dhtItem(threading.Thread):
    """ 
    class for dhtItems to initialize things properly from the 
    configuration dict, set up the labes for display and collect data/ 
    """
    def __init__(self, master, mq, dhtdef):
        self.messageQueue = Queue.Queue()
        self.masterQueue = mq
        self.temp = dht.dhtSensor('temperature',dhtdef)
        self.humi = dht.dhtSensor('humidity',dhtdef)
        self.sys = dhtdef['sys']
        self.id = dhtdef['id']
        self.logo = PhotoImage(file=dhtdef['logo'])
        self.image = Label(master,image=self.logo, background=bgcolor, foreground=fgcolor)
      
        self.idlabel = Label(master,text=self.id+"("+self.sys+")", justify=LEFT, background=bgcolor, foreground=fgcolor)
        self.idlabel.config(font=int(conf["fsize"]))
        self.tlabel = Label(master, text="", justify=RIGHT, background=bgcolor, foreground=fgcolor)
        self.tlabel.config(font=int(conf["fsize"]))
        self.hlabel = Label(master, text="", justify=RIGHT, background=bgcolor, foreground=fgcolor)
        self.hlabel.config(font=int(conf["fsize"]))
        self.tmlabel = Label(master, text="", justify=RIGHT, background=bgcolor, foreground=fgcolor)
        self.tmlabel.config(font=int(conf["fsize"]))
        self.event = threading.Event()
        threading.Thread.__init__(self)
        
    def run(self):
        while True:
            if self.event.isSet():
                #logging.info('{}: Thread returning. (done)'.format(self.sys))
                return
            try:
                m = self.masterQueue.get(block=False)
                if m[0] == 'quit':
                    self.event.set()
                    #logging.info('{}: quit message received.'.format(self.sys))
            except Queue.Empty:
                pass
            
            self.poll()
            self.event.wait(2)

    def poll(self):
		try:
		    t = self.temp.getData().value 
		    h = self.humi.getData().value 
		    tcolor = colors[self.temp.status+1]
		    hcolor = colors[self.humi.status+1]
		    
		    tstr = '{}@deg'.format(t).replace('@deg',degree_sign)
		    hstr = '{}%'.format(h)
		    
		except IOError as i:
			tstr = '!err {}'.format(i)
			tcolor = colors[2]
			hcolor = colors[2]
			hstr = ''
	    	
        
		self.tlabel.config(text=tstr, fg=tcolor)
		self.hlabel.config(text=hstr, fg=hcolor)
		self.tmlabel.config(text=str(time.strftime('%x %X', time.localtime(self.temp.stime))))

#
# This is our main class
#
class ourGUI:
    def __init__(self, master):
        self.masterQueue = Queue.Queue()
        self.master = master;
        master.title(conf["title"])
        self.dhtItems = [];
        self.label = Label(master, text="DHT11 Monitors")
        self.label.grid(row=0,column=0)
        self.label.config(font=int(conf["fsize"]))
        self.event = threading.Event()
        
        for i in range(len(conf["dhts"])):
            dht = conf["dhts"][i]
            dht["url"] = conf["baseurl"].replace('$sys',dht["sys"])
            d = dhtItem(master,self.masterQueue,dht)
            d.idlabel.grid(row=i,column=0)
            d.image.grid(row=i,column=1)
            d.tlabel.grid(row=i,column=2)
            d.hlabel.grid(row=i,column=3)
            d.tmlabel.grid(row=i,column=4)
            self.dhtItems.append(d)
            d.start()
            
        self.close = Button(master, text="Close", command=self.stop).grid(row=len(self.dhtItems)+2,column=4)
        threading.Timer(0.75,self.mainControl).start()
        
    def stop(self):
        self.masterQueue.put('stop')

    def mainControl(self):
        try:
            msg = self.masterQueue.get(block=True)
        except Queue.Empty:
            pass
        except KeyboardInterrupt:
            self.stopThreads()
            while len(dhtItems):
                pass
            sys.exit(0)
            
        m = self.masterQueue
        if msg == 'stop':
            self.master.quit()
        else:
            threading.Timer(0.75,self.mainControl).start()

    def stopThreads(self):
       for d in dhtItems:
            d.messageQueue.put(('quit',0))
            while d.isAlive():
                time.sleep(0.2)
            dhtItems.remove(d)
    
         
                    
root = Tk()
img = Image("photo", file=appicon)
root.tk.call('wm','iconphoto',root._w,img)

my_gui = ourGUI(root)

screenwidth = root.winfo_screenwidth()
windowwidth = root.winfo_width()
distance = screenwidth - windowwidth
root.geometry('+'+str(distance)+'+0')
root.configure(background=bgcolor)

try:
    root.mainloop()
except KeyboardInterrupt:
    print "KeyboardInterrupt"
    my_gui.stop()

