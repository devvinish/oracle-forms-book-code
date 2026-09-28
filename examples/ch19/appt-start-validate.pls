-- @where Trigger: WHEN-VALIDATE-ITEM on APPOINTMENTS.APPT_START
declare
  v_hour number := to_number(to_char(:appointments.appt_start, 'HH24.MI'));
begin
  if to_char(:appointments.appt_start, 'DY', 'nls_date_language=english') = 'SUN' then
    message('The clinic is closed on Sundays.');
    raise form_trigger_failure;
  elsif v_hour < 9 or v_hour >= 17 then
    message('Appointments start between 09:00 and 16:59.');
    raise form_trigger_failure;
  end if;
end;
