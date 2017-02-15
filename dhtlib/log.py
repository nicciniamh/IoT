import time
class logger:
    def __init__(self):
        self.log = []
    
    def message(self,text):
        self.log.append([time.time(),text])
        
    def logtext(self):
        t = ""
        for l in self.log:
            t = t + time.strftime("%x %X", time.localtime(l[0])) + ": " + l[1]+"\n"
        return t
    
    def tail(self,n=1):
        t = ""
        n = (len(self.log))-n;
        if(n < 0):
            n = 0
        for i in range(n,len(self.log)):
            l = self.log[i]
            t = t + time.strftime("%x %X", time.localtime(l[0])) + ": " + l[1]+"\n"
        return t;

if __name__ == "__main__":
    log = logger()
    log.message("Hello")
    log.message("Allow me to introduce myself");
    log.message("My name is Wyle E. Coyote");
    log.message("*explosion*");
    log.message("Allow me to introduce myself");
    log.message("My name is mud");
    print log.logtext()
    print "---"
    print log.tail(1)
    print "---"

    print log.tail(3)
