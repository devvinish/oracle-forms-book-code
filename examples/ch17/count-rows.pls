-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.COUNT_ROWS
declare
  v_table varchar2(30) := name_in('CTL.TABLE_NAME');   -- read an item by its name
  cur     exec_sql.curstype;
  v_count number;
  n       pls_integer;
begin
  if v_table is null then
    message('Choose a table first.');
    raise form_trigger_failure;
  end if;
  cur := exec_sql.open_cursor;
  exec_sql.parse(cur, 'select count(*) from ' || dbms_assert.simple_sql_name(v_table));
  exec_sql.define_column(cur, 1, v_count);
  n := exec_sql.execute(cur);
  if exec_sql.fetch_rows(cur) > 0 then
    exec_sql.column_value(cur, 1, v_count);
  end if;
  exec_sql.close_cursor(cur);
  copy(to_char(v_count, '99G999'), 'CTL.ROW_COUNT');     -- set an item by its name
end;
