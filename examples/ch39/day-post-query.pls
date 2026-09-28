-- @where Trigger: POST-QUERY on block APPOINTMENTS (form CH39_DAY)
select p.first_name || ' ' || p.last_name, d.first_name || ' ' || d.last_name
  into :appointments.patient_name, :appointments.doctor_name
  from patients p, doctors d
 where p.patient_id = :appointments.patient_id
   and d.doctor_id = :appointments.doctor_id;
:appointments.sel := 'N';     -- Initial Value is for new records only: a fetched record starts with null
