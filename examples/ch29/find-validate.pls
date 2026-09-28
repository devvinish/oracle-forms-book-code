-- @where Trigger: WHEN-VALIDATE-ITEM on CTL.FIND
declare
  v_find timer := find_timer('FIND');
begin
  -- GO_BLOCK and NEXT_RECORD are restricted here: a timer runs them just after
  if id_null(v_find) then
    v_find := create_timer('FIND', 1, no_repeat);
  else
    set_timer(v_find, 1, no_repeat);
  end if;
end;
