from formkit import *
f = form('CH28_PATIENT', 'CareWell Clinic')
main(f, 'Patients (object library)', 470, 220)
AttachedLibrary(f, 'cw_lib')
olb = ObjectLibrary.open('/work/forms/cw_objects.olb')
lib = dict([(o.getName(), o) for o in olb.getObjectLibraryObjects()])
for name in ['CW_NOTE', 'CW_CAUTION', 'CW_STOP']:          # subclassed, not copied
    Alert(f, name).setSubclassParent(lib[name])
VisualAttribute(f, 'CW_CURRENT_RECORD').setSubclassParent(lib['CW_CURRENT_RECORD'])
g = ObjectGroup(f, 'CW_STANDARD')                         # the objects every CareWell form needs
for child in ['CW_NOTE', 'CW_CAUTION', 'CW_STOP', 'CW_CURRENT_RECORD']:
    ObjectGroupChild(g, child)
p = block(f, 'PATIENTS', table='PATIENTS', records=8, where="city = 'Pune'", order='last_name, first_name', scroll=True)
p.setRecordVisualAttributeGroupName('CW_CURRENT_RECORD')
item(p, 'MRN', 'MRN', 12, 30, 70, length=10).setSubclassParent(lib['CW_READONLY'])
item(p, 'FIRST_NAME', 'First Name', 84, 30, 100, length=30)
item(p, 'LAST_NAME', 'Last Name', 186, 30, 100, length=30)
item(p, 'BIRTH_DATE', 'Born', 288, 30, 76, dt='date').setSubclassParent(lib['CW_DATE'])
trigger(p, 'KEY-DELREC', file='ch23/key-delrec.pls')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', "go_block('PATIENTS');\nexecute_query;")
save(f)
