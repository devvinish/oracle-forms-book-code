-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.APPTS (form CH24_PATIENTS)
declare
  v_list paramlist := get_parameter_list('CW_PATIENT');
  v_mode number := case :ctl.query_only when 'Y' then query_only else no_query_only end;
begin
  if not id_null(v_list) then
    destroy_parameter_list(v_list);                    -- left over from an earlier call
  end if;
  v_list := create_parameter_list('CW_PATIENT');
  add_parameter(v_list, 'P_PATIENT_ID', text_parameter, to_char(:patients.patient_id));
  cw_ctx.patient_id := :patients.patient_id;           -- library data (CW_LIB)
  :global.cw_appt_id := null;
  call_form('ch24_appointments', no_hide, no_replace, v_mode, share_library_data, v_list);
  -- runs when CH24_APPOINTMENTS has exited
  destroy_parameter_list(v_list);
  :ctl.chosen := :global.cw_appt_id;
end;
