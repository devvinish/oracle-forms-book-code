-- @where Trigger: WHEN-NEW-FORM-INSTANCE (form CH29_WAITING_ROOM)
declare
  v_clock timer;
begin
  set_application_property(client_idle_time, 20);  -- seconds without input: event IDLE
  go_block('APPOINTMENTS');
  execute_query;
  v_clock := create_timer('CLOCK', 1000, repeat);   -- every second, until deleted
end;
