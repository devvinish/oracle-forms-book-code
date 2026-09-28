-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.RUN (form CH33_REPORTS)
declare
  v_report  report_object := find_report_object('APPT_SCHEDULE');
  v_params  paramlist     := get_parameter_list('CW_REPORT');
  v_job     varchar2(100);
begin
  if not id_null(v_params) then
    destroy_parameter_list(v_params);
  end if;
  v_params := create_parameter_list('CW_REPORT');
  add_parameter(v_params, 'P_FROM', text_parameter, to_char(:ctl.p_from, 'YYYY-MM-DD'));
  add_parameter(v_params, 'P_TO', text_parameter, to_char(:ctl.p_to, 'YYYY-MM-DD'));
  add_parameter(v_params, 'PARAMFORM', text_parameter, 'NO');     -- no parameter form

  v_job := run_report_object(v_report, v_params);                  -- 'server_jobid'
  :ctl.job    := v_job;
  :ctl.status := report_object_status(v_job);
  if :ctl.status = 'FINISHED' then                                 -- show the output
    :ctl.url := 'http://localhost:9012/reports/rwservlet/getjobid'
             || substr(v_job, instr(v_job, '_', -1) + 1)
             || '?server=rep_wls_reports_formslab';
    web.show_document(:ctl.url, '_blank');
  end if;
end;
