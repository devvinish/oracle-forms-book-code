-- @where Trigger: WHEN-CUSTOM-JAVASCRIPT-EVENT (form level, form CH31_JS)
if :system.javascript_event_name = 'doctor' then
  :ctl.chosen := 'Dr. ' || :system.javascript_event_value;    -- sent by raiseEvent
  go_block('APPOINTMENTS');
  set_block_property('APPOINTMENTS', default_where,
    'doctor_id = (select doctor_id from doctors'
    || ' where substr(first_name, 1, 1) || ''. '' || last_name = '''
    || replace(:system.javascript_event_value, '''', '''''') || ''')'
    || ' and status = ''BOOKED'' and appt_start >= date ''2026-11-01'''
    || ' and appt_start < date ''2026-12-01''');
  execute_query;
end if;
