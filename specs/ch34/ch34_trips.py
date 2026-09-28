# CH34_TRIPS: eight items and a one-second clock, to count the requests the client sends
from formkit import *
f = form('CH34_TRIPS', 'CareWell Clinic')
main(f, 'Requests to the Forms Server', 420, 230)
c = block(f, 'CTL')
for i in range(1, 9):
    item(c, 'F%d' % i, 'Item %d' % i, 70, 10 + 22 * (i - 1), 120, edge='start')
s = item(c, 'START', 'Start Clock', 230, 10, 90, 20, kind='button')
t = item(c, 'STOP', 'Stop Clock', 230, 36, 90, 20, kind='button')
item(c, 'CLOCK', 'Clock', 270, 70, 70, kind='display', length=8, edge='start')
trigger(s, 'WHEN-BUTTON-PRESSED', file='ch34/start-clock.pls')
trigger(t, 'WHEN-BUTTON-PRESSED', "delete_timer('CLOCK');")
trigger(f, 'WHEN-TIMER-EXPIRED', ":ctl.clock := to_char(sysdate, 'HH24:MI:SS');")
save(f)
