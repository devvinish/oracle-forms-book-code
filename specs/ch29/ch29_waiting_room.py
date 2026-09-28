from formkit import *
f = form('CH29_WAITING_ROOM', 'CareWell Clinic')
main(f, 'Waiting Room - 3 November 2026', 470, 230)
c = block(f, 'CTL')
fi = item(c, 'FIND', 'Find patient', 70, 8, 100, length=30, edge='start')
item(c, 'NOW', 'Server time', 390, 8, 60, kind='display', length=8, edge='start')
item(c, 'INFO', None, 12, 178, 446, kind='display', length=100)
a = block(f, 'APPOINTMENTS', table='APPOINTMENTS', records=7, scroll=True,
          where="appt_start >= date '2026-11-03' and appt_start < date '2026-11-04'", order='appt_start')
a.setInsertAllowed(False); a.setUpdateAllowed(False); a.setDeleteAllowed(False)
item(a, 'APPT_START', 'Time', 12, 48, 40, dt='datetime', formatMask='HH24:MI')
item(a, 'PATIENT', 'Patient', 54, 48, 150, kind='display', length=61, db=False)
item(a, 'DOCTOR', 'Doctor', 206, 48, 110, kind='display', length=40, db=False)
item(a, 'STATUS', 'Status', 318, 48, 80, length=10)
for n in ['PATIENT_ID', 'DOCTOR_ID']:
    item(a, n, dt='number', cnv=None)
trigger(a, 'POST-QUERY', "select first_name || ' ' || last_name into :appointments.patient\n  from patients where patient_id = :appointments.patient_id;\n"
        "select 'Dr. ' || last_name into :appointments.doctor\n  from doctors where doctor_id = :appointments.doctor_id;")
e = Event(f, 'APPT_CHANGED')                       # database event: object change notification
e.setIntegerProperty(T.EVENT_TYPE_PTID, T.EVENT_TYPE_DATABASE_CTID)
e.setIntegerProperty(T.EVENT_DATABASE_SUB_TYPE_PTID, T.EVENT_DATABASE_SUB_TYPE_OCN_CTID)
e.setEventDbobjname('APPOINTMENTS')
for p in ['EVENT_OBJCHM_NTFUPD_PTID', 'EVENT_OBJCHM_NTFINS_PTID', 'EVENT_OBJCHM_NTFDEL_PTID', 'EVENT_ENABLED_PTID']:
    e.setBooleanProperty(getattr(T, p), True)
trigger(e, 'WHEN-EVENT-RAISED', file='ch29/appt-changed.pls')
i = Event(f, 'IDLE')                               # system event: the client is idle
i.setIntegerProperty(T.EVENT_TYPE_PTID, T.EVENT_TYPE_SYSTEMIDLE_CTID)
trigger(i, 'WHEN-EVENT-RAISED', file='ch29/idle.pls')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', file='ch29/new-form.pls')
trigger(f, 'WHEN-TIMER-EXPIRED', file='ch29/timer-expired.pls')
trigger(fi, 'WHEN-VALIDATE-ITEM', file='ch29/find-validate.pls')
save(f)
