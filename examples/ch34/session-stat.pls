-- @where Program unit SESSION_STAT (form CH34_PERF)
function session_stat(p_name varchar2) return number is
  v_value number;
begin
  select m.value into v_value                       -- this session's statistic
  from   v$mystat m, v$statname n
  where  n.statistic# = m.statistic# and n.name = p_name;
  return v_value;
end;
