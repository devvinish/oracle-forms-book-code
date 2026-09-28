# CH39_BOOKING: a department list that filters the doctors' LOV, a reason required only for cancelled
# appointments, and a check against double booking (Chapter 39, recipes 4-6)
from formkit import *
f = form('CH39_BOOKING', 'CareWell Clinic')
main(f, 'Appointments of a Patient', 630, 230)
c = block(f, 'CTL')
pp = ModuleParameter(f, 'P_PATIENT_ID')         # the patient, passed by the calling form
pp.setParameterDataType(T.PADA_NUMBER_CTID); pp.setParameterInitializeValue('10041')
item(c, 'PATIENT_NAME', 'Patient', 60, 10, 200, kind='display', length=60, edge='start')
a = block(f, 'APPOINTMENTS', table='APPOINTMENTS', records=6, where='patient_id = :parameter.p_patient_id',
          order='appt_start')
item(a, 'APPT_ID', None, dt='number', cnv=None)
item(a, 'PATIENT_ID', None, dt='number', cnv=None, initializeValue=':PARAMETER.P_PATIENT_ID')
item(a, 'DOCTOR_ID', None, dt='number', cnv=None, required=True)
dp = item(a, 'DEPT_ID', 'Department', 12, 50, 110, dt='number', kind='list', db=False,
          listStyle=T.LSST_POPLIST_CTID)
dp.insertElement(1, 'General Medicine', '100')
item(a, 'DOCTOR_NAME', 'Doctor', 124, 50, 120, length=61, db=False, lovName='LOV_DOCTORS',
     lovButton=True, validateFromList=True)
item(a, 'APPT_START', 'Starts', 246, 50, 104, dt='datetime', formatMask='DD-MON-YYYY HH24:MI', required=True)
item(a, 'DURATION_MIN', 'Min', 352, 50, 30, dt='number', initializeValue='15', required=True)
st = item(a, 'STATUS', 'Status', 384, 50, 88, kind='list', length=10, listStyle=T.LSST_POPLIST_CTID,
          initializeValue='BOOKED')
for i, (lbl, v) in enumerate([('Booked', 'BOOKED'), ('Checked in', 'CHECKED_IN'), ('Completed', 'COMPLETED'),
                              ('Cancelled', 'CANCELLED'), ('No-show', 'NO_SHOW')]):
    st.insertElement(i + 1, lbl, v)
item(a, 'REASON', 'Reason', 474, 50, 144, length=100)
lov(f, 'LOV_DOCTORS', "select first_name || ' ' || last_name as name, specialty, doctor_id from doctors "
    "where dept_id = :appointments.dept_id and active = 'Y' order by 1",
    [('NAME', 'Doctor', 120, 'APPOINTMENTS.DOCTOR_NAME'), ('SPECIALTY', 'Specialty', 110, None),
     ('DOCTOR_ID', 'ID', 0, 'APPOINTMENTS.DOCTOR_ID')], title='Doctors of the department', width=260, height=160)
trigger(a, 'POST-QUERY', file='ch39/booking-post-query.pls')
trigger(dp, 'WHEN-LIST-CHANGED', file='ch39/dept-changed.pls')
trigger(st, 'WHEN-LIST-CHANGED', file='ch39/status-changed.pls')
trigger(a, 'WHEN-VALIDATE-RECORD', 'check_double_booking;')
trigger(a, 'PRE-INSERT', file='ch39/booking-pre-insert.pls')
trigger(a, 'PRE-UPDATE', 'check_double_booking;')
unit(f, 'SET_REASON_REQUIRED', file='ch39/set-reason-required.pls')
unit(f, 'CHECK_DOUBLE_BOOKING', file='ch39/check-double-booking.pls')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', """declare
  v_rg recordgroup := create_group_from_query('RG_DEPTS',
           'select dept_name, to_char(dept_id) from departments order by dept_id');
begin
  if populate_group(v_rg) = 0 then
    populate_list('APPOINTMENTS.DEPT_ID', v_rg);
  end if;
  select first_name || ' ' || last_name into :ctl.patient_name
    from patients where patient_id = :parameter.p_patient_id;
  go_block('APPOINTMENTS');
  execute_query;
end;""")
save(f)
