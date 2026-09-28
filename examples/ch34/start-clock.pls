-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.START (form CH34_TRIPS)
declare
  v_timer timer;
begin
  v_timer := create_timer('CLOCK', 1000, repeat);   -- every second
end;
