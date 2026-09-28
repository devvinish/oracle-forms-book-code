from formkit import *
f = form('CH11_CHART', 'CareWell Clinic')
main(f, 'Appointments by Department', 460, 220)
b = block(f, 'BARS', records=8)
item(b, 'DEPT_NAME', 'Department', 12, 28, 110, length=40, insertAllowed=False, updateAllowed=False)
item(b, 'APPTS', 'Appointments', 124, 28, 60, dt='number', kind='display', justification=T.JUSTIFICATION_RIGHT_CTID)
item(b, 'BAR', None, 190, 28, 250, kind='display', length=160, foregroundColor='r25g50b75')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', file='ch11/chart-fill.pls')
save(f)
