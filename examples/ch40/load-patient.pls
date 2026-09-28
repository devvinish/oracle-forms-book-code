-- @where Program unit: procedure LOAD_PATIENT (form CW_APPOINTMENTS)
-- shows the appointments of the current patient: when the form starts, and when the user comes back
-- to it after choosing another patient in CW_PATIENTS
procedure load_patient is
begin
  if cw_ctx.patient_id is null then
    message('Choose a patient in Patients first.');
  elsif :ctl.patient_id is null or :ctl.patient_id <> cw_ctx.patient_id then
    :ctl.patient_id := cw_ctx.patient_id;
    select first_name || ' ' || last_name || '  (' || mrn || ')' into :ctl.patient_name
      from patients where patient_id = :ctl.patient_id;
    go_block('APPOINTMENTS');
    execute_query;                       -- asks first whether to save changes for the previous patient
  end if;
end;
