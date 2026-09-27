-- @where Trigger: WHEN-VALIDATE-ITEM on DEPARTMENTS.HEAD_DOCTOR
declare
  v_name varchar2(61);
  v_dept doctors.dept_id%type;
begin
  select first_name || ' ' || last_name, dept_id
  into   v_name, v_dept
  from   doctors
  where  doctor_id = :departments.head_doctor;

  if v_dept <> :departments.dept_id then
    message('Doctor ' || :departments.head_doctor || ' works in another department.');
    raise form_trigger_failure;
  end if;
  :departments.head_name := v_name;
exception
  when no_data_found then
    message('There is no doctor ' || :departments.head_doctor || '.');
    raise form_trigger_failure;
end;
