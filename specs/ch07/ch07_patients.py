from formkit import *
f = form('CH07_PATIENTS', 'CareWell Clinic')
main(f, 'Patients', 560, 280)
flt = block(f, 'FILTER')
item(flt, 'CITY', 'City', 60, 10, 110, length=30, edge='start')
btn = item(flt, 'FIND', 'Find', 180, 10, 60, 18, kind='button')
item(flt, 'LAST_QUERY', 'Last query', 16, 214, 508, 52, length=2000, multiLine=True,
     insertAllowed=False, updateAllowed=False, keyboardNavigable=False)
p = block(f, 'PATIENTS', table='PATIENTS', records=8, order='last_name, first_name', scroll=True)
item(p, 'PATIENT_ID', 'ID', 16, 58, 44, dt='number', insertAllowed=False, updateAllowed=False,
     keyboardNavigable=False)
item(p, 'MRN', 'MRN', 62, 58, 64, length=10, insertAllowed=False, updateAllowed=False,
     keyboardNavigable=False)
item(p, 'FIRST_NAME', 'First Name', 128, 58, 74, length=30)
item(p, 'LAST_NAME', 'Last Name', 204, 58, 74, length=30)
item(p, 'GENDER', 'G', 280, 58, 20, length=1)
item(p, 'BIRTH_DATE', 'Birth Date', 302, 58, 66, dt='date')
item(p, 'CITY', 'City', 370, 58, 70, length=30)
item(p, 'PHONE', 'Phone', 442, 58, 72, length=20)
p.setScrollbarXPosition(518); p.setScrollbarYPosition(58); p.setScrollbarLength(128); p.setScrollbarWidth(10)
trigger(p, 'PRE-INSERT', file='ch07/patients-pre-insert.pls')
trigger(btn, 'WHEN-BUTTON-PRESSED', file='ch07/find-by-city.pls')
save(f)
