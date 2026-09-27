-- @where Trigger: WHEN-NEW-FORM-INSTANCE on the form
declare
  v_max number;
begin
  select max(count(*)) into v_max
  from   appointments a, doctors d
  where  d.doctor_id = a.doctor_id
  group  by d.dept_id;

  go_block('BARS');
  for r in (select dp.dept_name, count(*) as appts
            from   appointments a, doctors d, departments dp
            where  d.doctor_id = a.doctor_id
            and    dp.dept_id = d.dept_id
            group  by dp.dept_name
            order  by appts desc) loop
    if :bars.dept_name is not null then
      create_record;
    end if;
    :bars.dept_name := r.dept_name;
    :bars.appts     := r.appts;
    for i in 1 .. round(r.appts / v_max * 36) loop     -- one block character per step
      :bars.bar := :bars.bar || unistr('\2588');
    end loop;
  end loop;
  first_record;
end;
