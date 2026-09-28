-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.PRINT (form CH37_LEGACY, before the upgrade)
declare
  v_params paramlist;
  v_button number;
begin
  v_params := create_parameter_list('TMPDATA');
  add_parameter(v_params, 'P_FROM', text_parameter, '2026-11-16');
  add_parameter(v_params, 'P_TO', text_parameter, '2026-11-22');
  add_parameter(v_params, 'PARAMFORM', text_parameter, 'NO');
  run_product(REPORTS, '/work/reports/cw_appt_schedule', SYNCHRONOUS, RUNTIME,
              FILESYSTEM, v_params, NULL);
  destroy_parameter_list(v_params);
  change_alert_message('CW_NOTE', 'The schedule was printed.');
  v_button := show_alert('CW_NOTE');
end;
