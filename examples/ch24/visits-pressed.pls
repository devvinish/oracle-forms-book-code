-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.VISITS (form CH24_PATIENTS)
declare
  v_list paramlist := get_parameter_list('CW_VISITS');
begin
  if not id_null(v_list) then
    destroy_parameter_list(v_list);
  end if;
  v_list := create_parameter_list('CW_VISITS');
  add_parameter(v_list, 'P_PATIENT_ID', text_parameter, to_char(:patients.patient_id));
  open_form('ch16_visits', activate, no_session, v_list);
  message('OPEN_FORM returned');
end;
