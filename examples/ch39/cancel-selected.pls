-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.CANCEL_SELECTED (form CH39_DAY)
declare
  v_n pls_integer := 0;
begin
  if nvl(:ctl.selected, 0) = 0 then
    message('Check the appointments to cancel first.');
    return;
  end if;
  set_alert_property('CONFIRM', ALERT_MESSAGE_TEXT,
                     'Cancel ' || :ctl.selected || ' appointments of ' || to_char(:ctl.day, 'DD-MON-YYYY') || '?');
  if show_alert('CONFIRM') <> ALERT_BUTTON1 then
    return;
  end if;
  go_block('APPOINTMENTS');
  first_record;
  loop
    if :appointments.sel = 'Y' then
      :appointments.status := 'CANCELLED';
      :appointments.reason := 'Doctor unavailable';
      v_n := v_n + 1;
    end if;
    exit when :system.last_record = 'TRUE';
    next_record;
  end loop;
  :system.message_level := '5';        -- the message below replaces FRM-40400
  commit_form;
  :system.message_level := '0';
  if :system.form_status = 'QUERY' then       -- saved
    message(v_n || ' appointments cancelled.');
    :ctl.selected := 0;
    execute_query;
  end if;
end;
