from formkit import *
f = form('CH19_APPOINTMENT', 'CareWell Clinic')
main(f, 'Appointments', 560, 220)
a = block(f, 'APPOINTMENTS', table='APPOINTMENTS', records=6, scroll=True,
          where="doctor_id = 1003 and appt_start >= date '2026-10-01'", order='appt_start')
item(a, 'APPT_ID', 'ID', 12, 24, 44, dt='number', insertAllowed=False, updateAllowed=False, keyboardNavigable=False)
item(a, 'DOCTOR_ID', 'Doctor', 58, 24, 40, dt='number', required=True, initializeValue='1003')
item(a, 'PATIENT_ID', 'Patient', 100, 24, 46, dt='number', required=True)
item(a, 'APPT_START', 'Start', 148, 24, 110, dt='datetime', formatMask='DD-MON-YYYY HH24:MI', required=True)
item(a, 'DURATION_MIN', 'Min', 260, 24, 30, dt='number', required=True, initializeValue='15',
     lowestAllowedValue='5', highestAllowedValue='240')
st = item(a, 'STATUS', 'Status', 292, 24, 90, kind='list', length=10, required=True, initializeValue='BOOKED',
          listStyle=T.LSST_POPLIST_CTID)
for i, s in enumerate(['BOOKED', 'CHECKED_IN', 'COMPLETED', 'CANCELLED', 'NO_SHOW']):
    st.insertElement(i + 1, s.replace('_', ' ').title().replace('In', 'in'), s)
item(a, 'REASON', 'Reason', 384, 24, 150, length=100)
a.setScrollbarXPosition(536); a.setScrollbarYPosition(24); a.setScrollbarLength(96); a.setScrollbarWidth(10)
trigger(Item.find(a, 'APPT_START'), 'WHEN-VALIDATE-ITEM', file='ch19/appt-start-validate.pls')
trigger(st, 'WHEN-VALIDATE-ITEM', file='ch19/status-validate.pls')
trigger(a, 'WHEN-VALIDATE-RECORD', file='ch19/appointments-validate-record.pls')
trigger(a, 'PRE-INSERT', file='ch15/appointments-pre-insert.pls')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', "go_block('APPOINTMENTS');\nexecute_query;")
save(f)
