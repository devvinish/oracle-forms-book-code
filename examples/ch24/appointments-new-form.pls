-- @where Trigger: WHEN-NEW-FORM-INSTANCE (form CH24_APPOINTMENTS)
begin
  select first_name || ' ' || last_name into :ctl.patient
    from patients where patient_id = :parameter.p_patient_id;
  :ctl.info := 'Called by ' || nvl(get_application_property(calling_form), 'no form')
            || ';  CW_CTX.PATIENT_ID = ' || nvl(to_char(cw_ctx.patient_id), 'null');
  go_block('APPOINTMENTS');
  execute_query;
end;
