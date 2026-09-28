# CH37_LEGACY: a form written the way older releases allowed, to upgrade in Chapter 37
from formkit import *
f = form('CH37_LEGACY', 'CareWell Clinic')
main(f, 'Weekly Schedule (legacy code)', 400, 120)
c = block(f, 'CTL')
p = item(c, 'PRINT', 'Print Schedule', 20, 20, 110, 20, kind='button')
s = item(c, 'SAVE', 'Save', 150, 20, 80, 20, kind='button')
alert(f, 'CW_NOTE', 'CareWell Clinic', 'Done.')
trigger(p, 'WHEN-BUTTON-PRESSED', file='ch37/legacy-print.pls')
trigger(s, 'WHEN-BUTTON-PRESSED', file='ch37/legacy-save.pls')
save(f)
