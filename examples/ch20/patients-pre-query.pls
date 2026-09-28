-- @where Trigger: PRE-QUERY on PATIENTS
declare
  v_age varchar2(10) := :ctl.age;           -- a criterion the table has no column for
begin
  if v_age is not null then
    set_block_property('PATIENTS', onetime_where,
      'birth_date >  add_months(trunc(sysdate), -12 * (' || to_number(v_age) || ' + 1)) ' ||
      'and birth_date <= add_months(trunc(sysdate), -12 * ' || to_number(v_age) || ')');
  end if;
end;
