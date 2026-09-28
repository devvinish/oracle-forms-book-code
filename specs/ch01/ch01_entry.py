from formkit import *
f = form('CH01_ENTRY', 'Chapter 1')
main(f, 'GET_APPLICATION_PROPERTY', 420, 120)
b = block(f, 'CTRL')
item(b, 'DUMMY', 'An item for the cursor', 20, 40, 200)
trigger(f, 'WHEN-NEW-FORM-INSTANCE', file='ch01/entry-new-form-instance.pls')
save(f)
