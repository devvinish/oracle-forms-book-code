from formkit import *
f = form('CH15_BOOKING', 'CareWell Clinic')
main(f, 'Book an Appointment', 480, 250)
a = block(f, 'APPOINTMENTS', table='APPOINTMENTS')
a.setQueryAllowed(False); a.setUpdateAllowed(False); a.setDeleteAllowed(False)
item(a, 'APPT_ID', 'Appointment', 90, 12, 60, dt='number', kind='display', edge='start', db=True)
item(a, 'PATIENT_ID', dt='number', cnv=None)
item(a, 'DOCTOR_ID', dt='number', cnv=None)
pn = item(a, 'PATIENT_NAME', 'Patient', 90, 36, 170, length=61, db=False, edge='start',
          lovName='LOV_PATIENTS', validateFromList=True, lovButton=True, required=True,
          hint='Type part of the name and press Tab, or press Ctrl+L for the list')
item(a, 'MRN', None, 266, 36, 70, length=10, kind='display', db=False)
dn = item(a, 'DOCTOR_NAME', 'Doctor', 90, 60, 170, length=61, db=False, edge='start',
          lovName='LOV_DOCTORS', validateFromList=True, lovButton=True, required=True)
item(a, 'SPECIALTY', None, 266, 60, 170, length=40, kind='display', db=False)
item(a, 'APPT_START', 'Start', 90, 84, 110, dt='datetime', formatMask='DD-MON-YYYY HH24:MI',
     edge='start', required=True)
item(a, 'DURATION_MIN', 'Minutes', 90, 108, 40, dt='number', edge='start', initializeValue='15',
     lovName='LOV_DURATIONS', lovButton=True)
item(a, 'ROOM_NO', 'Room', 90, 132, 60, length=6, edge='start', lovName='LOV_ROOMS',
     validateFromList=True, lovButton=True)
item(a, 'REASON', 'Reason', 90, 156, 300, length=100, edge='start')

l = lov(f, 'LOV_PATIENTS',
        "select name, mrn, city, patient_id from "
        "(select first_name || ' ' || last_name as name, mrn, city, patient_id from patients) "
        "order by name",
        [('NAME', 'Patient', 150, 'APPOINTMENTS.PATIENT_NAME'), ('MRN', 'MRN', 70, 'APPOINTMENTS.MRN'),
         ('CITY', 'City', 90, None), ('PATIENT_ID', 'ID', 0, 'APPOINTMENTS.PATIENT_ID')],
        title='Patients', width=340, height=260)
l.setFilterBeforeDisplay(True)
l = lov(f, 'LOV_DOCTORS',
        "select name, specialty, dept_name, consult_fee, doctor_id from "
        "(select d.first_name || ' ' || d.last_name as name, d.specialty, p.dept_name, "
        "d.consult_fee, d.doctor_id from doctors d, departments p "
        "where p.dept_id = d.dept_id and d.active = 'Y') order by name",
        [('NAME', 'Doctor', 120, 'APPOINTMENTS.DOCTOR_NAME'), ('SPECIALTY', 'Specialty', 140, 'APPOINTMENTS.SPECIALTY'),
         ('DEPT_NAME', 'Department', 100, None), ('CONSULT_FEE', 'Fee', 40, None),
         ('DOCTOR_ID', 'ID', 0, 'APPOINTMENTS.DOCTOR_ID')],
        title='Doctors', width=440, height=260)
l.setAutoColumnWidth(True)
l = lov(f, 'LOV_ROOMS',
        "select room_no, room_type from rooms where dept_id = "
        "(select dept_id from doctors where doctor_id = :appointments.doctor_id) order by room_no",
        [('ROOM_NO', 'Room', 50, 'APPOINTMENTS.ROOM_NO'), ('ROOM_TYPE', 'Type', 80, None)],
        title='Rooms of the Doctor\'s Department', width=220, height=160)
l.setAutoRefresh(True)
lov(f, 'LOV_DURATIONS',
    "select 15 as minutes, 'Follow-up' as description from dual",
    [('MINUTES', 'Minutes', 50, 'APPOINTMENTS.DURATION_MIN'), ('DESCRIPTION', 'Kind', 100, None)],
    title='Durations', width=200, height=180)
trigger(a, 'PRE-INSERT', file='ch15/appointments-pre-insert.pls')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', file='ch15/durations-group.pls')
save(f)
