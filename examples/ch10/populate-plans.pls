-- @where Trigger: WHEN-NEW-FORM-INSTANCE on the form
declare
  rg     recordgroup;
  status number;
begin
  rg := create_group_from_query('RG_PLANS',
          'select provider || '' - '' || plan_name, to_char(plan_id) ' ||
          'from insurance_plans order by provider, plan_name');
  status := populate_group(rg);
  if status = 0 then
    populate_list('PATIENTS.PLAN_ID', rg);
  end if;
  go_block('PATIENTS');
  execute_query;
end;
