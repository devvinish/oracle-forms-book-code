-- @where Program unit MEASURE (form CH34_PERF)
procedure measure(p_mode varchar2, p_label varchar2) is
  v_start number; v_trips number; v_execs number;
begin
  :ctl.mode := p_label;
  v_trips := session_stat('SQL*Net roundtrips to/from client');
  v_execs := session_stat('execute count');
  v_start := dbms_utility.get_time;                 -- centiseconds
  go_block('APPTS');
  execute_query;
  last_record;                                      -- fetches every row
  :ctl.cs    := dbms_utility.get_time - v_start;
  :ctl.trips := session_stat('SQL*Net roundtrips to/from client') - v_trips;
  :ctl.execs := session_stat('execute count') - v_execs;
  :ctl.rows  := :system.cursor_record;
  first_record;
end;
