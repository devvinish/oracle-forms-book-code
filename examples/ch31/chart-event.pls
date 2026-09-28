-- @where Trigger: WHEN-CUSTOM-ITEM-EVENT on CTL.CHART
declare
  v_params paramlist := get_parameter_list(:system.custom_item_event_parameters);
  v_type   number;
  v_label  varchar2(100);
begin
  if :system.custom_item_event = 'BAR_CLICKED' then
    get_parameter_attr(v_params, 'BAR_LABEL', v_type, v_label);
    :ctl.chosen := 'Dr. ' || v_label;                   -- 'M. Wilson'
    go_block('APPOINTMENTS');
    set_block_property('APPOINTMENTS', default_where,
      'doctor_id = (select doctor_id from doctors'
      || ' where substr(first_name, 1, 1) || ''. '' || last_name = '''
      || replace(v_label, '''', '''''') || ''') and status = ''BOOKED'''
      || ' and appt_start >= date ''2026-11-01'' and appt_start < date ''2026-12-01''');
    execute_query;
  end if;
end;
