# Finishes the form that the wizards built in Forms Builder (Chapter 8): the window title, the name
# of the head doctor next to the key, and the checks of the head doctor. Safe to run again.
from formkit import *
start()
f = FormModule.open('/work/forms/ch08_departments.fmb')
Window.find(f, 'WINDOW1').setTitle('CareWell Clinic - Departments')
b = Block.find(f, 'DEPARTMENTS')
if Item.find(b, 'HEAD_NAME') is None:
    item(b, 'HEAD_NAME', None, 130, 61, 140, 15, kind='display', length=61, cnv='CANVAS4', db=False)
def set_trigger(owner, name, file):
    t = Trigger.find(owner, name)
    if t is None: trigger(owner, name, file=file)
    else: t.setTriggerText(code_of(file))
set_trigger(b, 'POST-QUERY', 'ch08/departments-post-query.pls')
set_trigger(Item.find(b, 'HEAD_DOCTOR'), 'WHEN-VALIDATE-ITEM', 'ch08/head-doctor-validate.pls')
save(f)
