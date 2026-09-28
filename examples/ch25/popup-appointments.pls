-- @where Popup menu POP_PATIENT: item APPOINTMENTS (Menu Item Code)
declare
  v_list paramlist := get_parameter_list('CW_PATIENT');
begin
  if not id_null(v_list) then
    destroy_parameter_list(v_list);
  end if;
  v_list := create_parameter_list('CW_PATIENT');
  add_parameter(v_list, 'P_PATIENT_ID', text_parameter, :patients.patient_id);
  call_form('ch24_appointments', no_hide, no_replace, no_query_only, v_list);
end;
