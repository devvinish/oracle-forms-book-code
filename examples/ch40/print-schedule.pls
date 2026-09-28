-- @where Program unit: procedure PRINT_SCHEDULE (form CW_MAIN)
-- today's schedule as a PDF, with the report of Chapter 33
procedure print_schedule is
  v_params paramlist := get_parameter_list('CW_REPORT');
  v_job    varchar2(100);
begin
  if not id_null(v_params) then
    destroy_parameter_list(v_params);
  end if;
  v_params := create_parameter_list('CW_REPORT');
  add_parameter(v_params, 'P_FROM', text_parameter, to_char(sysdate, 'YYYY-MM-DD'));
  add_parameter(v_params, 'P_TO', text_parameter, to_char(sysdate, 'YYYY-MM-DD'));
  add_parameter(v_params, 'PARAMFORM', text_parameter, 'NO');
  v_job := run_report_object(find_report_object('APPT_SCHEDULE'), v_params);
  if report_object_status(v_job) = 'FINISHED' then
    message('Schedule ready: job ' || substr(v_job, instr(v_job, '_', -1) + 1)
            || ' of ' || substr(v_job, 1, instr(v_job, '_', -1) - 1));
    -- web.show_document(<the job's getjobid URL>, '_blank') opens it in the user's browser
  else
    message('The schedule could not be printed: ' || report_object_status(v_job));
  end if;
end;
