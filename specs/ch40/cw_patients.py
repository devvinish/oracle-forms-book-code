# CW_PATIENTS: find a patient, and open the patient's appointments or invoices (Chapter 40)
from formkit import *
f = from_template('/work/forms/cw_template.fmb', 'CW_PATIENTS', 'Patients', 560, 330)
f.setMenuModule('cw_app')
c = block(f, 'CTL')
frame(f, 'FR_FIND', 'Find patients whose', 8, 6, 544, 78)
item(c, 'NAME', 'Name contains', 90, 22, 150, length=40, edge='start')
item(c, 'CITY', 'City', 300, 22, 110, length=30, edge='start')
item(c, 'BORN_FROM', 'Born from', 90, 50, 80, dt='date', formatMask='DD-MON-YYYY', edge='start')
item(c, 'BORN_TO', 'to', 196, 50, 80, dt='date', formatMask='DD-MON-YYYY', edge='start')
b = item(c, 'FIND', 'Find', 300, 48, 60, 22, kind='button', mouseNavigate=False, keyboardNavigable=False)
trigger(b, 'WHEN-BUTTON-PRESSED', 'find_patients;')
item(c, 'COUNTER', None, 12, 280, 160, kind='display', length=40)
item(c, 'TOTAL', None, dt='number', cnv=None)
for name, text, x, form in [('APPTS', 'Appointments...', 300, 'cw_appointments'), ('BILLS', 'Invoices...', 420, 'cw_billing')]:
    b = item(c, name, text, x, 276, 110, 24, kind='button', mouseNavigate=False, keyboardNavigable=False)
    trigger(b, 'WHEN-BUTTON-PRESSED', "cw_nav.open_module('%s', :patients.patient_id);" % form)
p = block(f, 'PATIENTS', table='PATIENTS', records=9, order='last_name, first_name', scroll=True)
p.setInsertAllowed(False); p.setDeleteAllowed(False)
item(p, 'PATIENT_ID', None, dt='number', cnv=None)
item(p, 'MRN', 'MRN', 12, 102, 70, length=10, updateAllowed=False)
item(p, 'LAST_NAME', 'Last Name', 84, 102, 100, length=30, updateAllowed=False)
item(p, 'FIRST_NAME', 'First Name', 186, 102, 90, length=30, updateAllowed=False)
item(p, 'CITY', 'City', 278, 102, 90, length=30)
item(p, 'PHONE', 'Phone', 370, 102, 100, length=20)
item(p, 'PLAN_ID', 'Plan', 472, 102, 60, dt='number')
p.setScrollbarXPosition(540); p.setScrollbarYPosition(102); p.setScrollbarLength(148); p.setScrollbarWidth(10)
trigger(p, 'WHEN-NEW-RECORD-INSTANCE', file='ch39/counter.pls')
unit(f, 'FIND_PATIENTS', file='ch39/find-patients.pls')
Trigger.find(f, 'WHEN-NEW-FORM-INSTANCE').setTriggerText(
    "cw_nav.start_form(:parameter.p_user);\n"
    "if not cw_sec.has_role('ADMIN,BILLING') then\n"
    "  set_item_property('CTL.BILLS', ENABLED, PROPERTY_FALSE);\n"
    "end if;\n"
    "find_patients;")
save(f)
