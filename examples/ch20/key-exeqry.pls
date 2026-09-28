-- @where Trigger: KEY-EXEQRY on PATIENTS
begin
  execute_query;
  :ctl.last_query := get_block_property('PATIENTS', last_query);
  :ctl.hits       := get_block_property('PATIENTS', query_hits);
end;
