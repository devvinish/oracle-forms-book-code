from formkit import *
f = form('CH18_TRACE', 'CareWell Clinic')
main(f, 'Trigger Trace', 440, 170)
d = block(f, 'DOCTORS', table='DOCTORS', records=3, where='doctor_id <= 1002', order='doctor_id')
item(d, 'DOCTOR_ID', 'ID', 12, 26, 40, dt='number', updateAllowed=False)
item(d, 'FIRST_NAME', 'First Name', 54, 26, 90, length=30)
ln = item(d, 'LAST_NAME', 'Last Name', 146, 26, 90, length=30)
item(d, 'PHONE', 'Phone', 238, 26, 110, length=20)
unit(f, 'TRACE', file='ch18/trace-spec.pls')
unit(f, 'TRACE', file='ch18/trace-body.pls')
def t(owner, name, extra=''):
    return trigger(owner, name, "trace.log('%s');%s" % (name, extra))
for n in ['PRE-FORM', 'WHEN-NEW-FORM-INSTANCE', 'PRE-BLOCK', 'POST-BLOCK', 'WHEN-NEW-BLOCK-INSTANCE',
          'PRE-RECORD', 'POST-RECORD', 'WHEN-NEW-RECORD-INSTANCE', 'PRE-TEXT-ITEM', 'POST-TEXT-ITEM',
          'WHEN-NEW-ITEM-INSTANCE', 'WHEN-VALIDATE-ITEM', 'WHEN-VALIDATE-RECORD', 'PRE-COMMIT',
          'POST-FORMS-COMMIT', 'POST-DATABASE-COMMIT', 'POST-FORM']:
    t(f, n)
t(f, 'KEY-COMMIT', '\ncommit_form;')
for n in ['PRE-QUERY', 'POST-QUERY', 'PRE-UPDATE', 'POST-UPDATE']:
    t(d, n)
it = trigger(ln, 'WHEN-NEW-ITEM-INSTANCE', "trace.log('WHEN-NEW-ITEM-INSTANCE*');")
it.setExecuteHierarchy(T.EXHI_AFTER_CTID)
save(f)
