-- @where Trigger: POST-QUERY on block APPOINTMENTS (form CH39_BOOKING)
select d.dept_id, d.first_name || ' ' || d.last_name
  into :appointments.dept_id, :appointments.doctor_name
  from doctors d
 where d.doctor_id = :appointments.doctor_id;
set_reason_required;
