-- @where Trigger: WHEN-NEW-FORM-INSTANCE on the form
begin
  select first_name || ' ' || last_name || '  (' || mrn || ')'
  into   :ctl.patient
  from   patients
  where  patient_id = :parameter.p_patient_id;

  go_block('VISITS');
  execute_query;
exception
  when no_data_found then
    message('There is no patient ' || :parameter.p_patient_id || '.');
end;
