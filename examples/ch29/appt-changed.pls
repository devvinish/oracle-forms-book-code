-- @where Trigger: WHEN-EVENT-RAISED on event APPT_CHANGED
:ctl.info := 'Appointments changed at ' || to_char(sysdate, 'HH24:MI:SS')
              || ': list refreshed';
go_block('APPOINTMENTS');
execute_query;
