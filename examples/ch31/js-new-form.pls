-- @where Trigger: WHEN-NEW-FORM-INSTANCE (form CH31_JS)
declare
  v_timer timer;
begin
  v_timer := create_timer('WJSI_JOIN', 1000, repeat);   -- see WHEN-TIMER-EXPIRED
end;
