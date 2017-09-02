#
# This script is meant to run under sentest.py. It will not run with straight python
# as none of the global variables used would exist and it makes no sense anyway. 
#
if not 'last_switch' in stateData.keys():
    last_switch = 0

if not 'last_state' in stateData.keys():
    last_state = None

fan_delay = 30
fan_on = 70
now = int(time.time())
time_diff = now - last_switch
temp = Living_Room__temp_.value
fan_state = True if fan_control.getData().value else False
fan_next = fan_delay - time_diff

if last_state == None:
    if temp >= fan_on:
        pstate = 'fan_set'
        state = True
    else:
        pstate = 'fan_set'
        state = False

print 'fan_control entr {} {} {} {} {:.2f}'.format(now,temp,pstate,fan_state,fan_next)
if pstate == 'fan_next':
    if time_diff > fan_delay:
        pstate = 'fan_set'
    else:
        pstate = 'fan_next'

if pstate == 'fan_set':
    if fan_state != state or last_state == None:
        print 'setting fan_control to','on' if state else 'off'
        fan_control.sendData(state)
        fan_state = True if fan_control.getData().value else False
    last_switch = now
    time_diff = 0
    print pstate,'setting last_switch to {} and time_diff to {}'.format(last_switch,time_diff)
    pstate = 'fan_next'

last_state = state
fan_next = fan_delay - time_diff
print 'fan_control exit {} {} {} {} {:.2f}'.format(now,temp,pstate,fan_state,fan_next)
