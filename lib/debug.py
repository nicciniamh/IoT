import pprint

def debug(*args):
    debugFlag = args[0]
    if not debugFlag:
        return
    s = ''
    for i in range(1,len(args)):
        s = '{} {}'.format(s,pprint.pformat(args[i]))
    s = 'DEBUG: {}'.format(s)
    if len(s):
        print(s)
        