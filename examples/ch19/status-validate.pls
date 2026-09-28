-- @where Trigger: WHEN-VALIDATE-ITEM on APPOINTMENTS.STATUS
declare
  v_old varchar2(10) := get_item_property('APPOINTMENTS.STATUS', database_value);
begin
  if :appointments.status = v_old then
    return;                                            -- changed back: nothing to check
  elsif v_old in ('COMPLETED', 'CANCELLED', 'NO_SHOW') then
    message('A ' || lower(v_old) || ' appointment can''t change its status.');
    raise form_trigger_failure;
  elsif v_old = 'BOOKED' and :appointments.status = 'COMPLETED' then
    message('Check the patient in before completing the appointment.');
    raise form_trigger_failure;
  end if;
end;
