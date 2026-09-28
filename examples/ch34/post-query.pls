-- @where Trigger: POST-QUERY on APPTS (form CH34_PERF)
if :ctl.mode = 'Three queries' then
  select first_name || ' ' || last_name into :appts.patient
  from   patients where patient_id = :appts.patient_id;
  select 'Dr. ' || last_name into :appts.doctor
  from   doctors where doctor_id = :appts.doctor_id;
  select max(i.total_amount) into :appts.billed
  from   visits v, invoices i
  where  i.visit_id = v.visit_id and v.appt_id = :appts.appt_id;
elsif :ctl.mode = 'One call' then
  cw_api.appt_details(:appts.appt_id, :appts.patient, :appts.doctor, :appts.billed);
end if;
