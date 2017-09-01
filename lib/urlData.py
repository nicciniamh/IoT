import json, urllib, sys, re

class dataException(Exception):
    pass

def getData(url):
    ''' Read data from a uri and return it. 
        Possible excpetions:
        dataException - when status is not 'ok'
    '''
    try:
        if not re.match(r'(https?://\S+)', url):
            if 'file://' in url:
                url = url.replace('file://','',1)
            url = url.split('?')[0] # Query strings make no sense for file like objects. 
            rsp = open(url).read()
        else:
            rsp = urllib.urlopen(url).read()

    except Exception as e:
        raise dataException(repr(e))

    data = json.loads(rsp)
    if data["status"] != "ok":
        if error in data:
            error = data['error']
        else:
            error = "Data validation error"
        raise dataException(error)
    return data


