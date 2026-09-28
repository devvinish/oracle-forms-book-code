from formkit import *
f = form('CH31_PJC', 'CareWell Clinic')
main(f, 'Patient Phones (PJC)', 420, 200)
p = block(f, 'PATIENTS', table='PATIENTS', records=6, where="city = 'Pune'", order='last_name, first_name', scroll=True)
item(p, 'FIRST_NAME', 'First Name', 12, 30, 100, length=30)
item(p, 'LAST_NAME', 'Last Name', 114, 30, 100, length=30)
ph = item(p, 'PHONE', 'Phone', 216, 30, 110, length=20)
ph.setImplementationClass('cw.PhoneField')          # a pluggable Java component
trigger(f, 'WHEN-NEW-FORM-INSTANCE', "go_block('PATIENTS');\nexecute_query;")
save(f)
