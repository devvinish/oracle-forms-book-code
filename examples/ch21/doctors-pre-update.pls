-- @where Trigger: PRE-UPDATE on DOCTORS
declare
  v_old varchar2(20) := get_item_property('DOCTORS.CONSULT_FEE', database_value);
begin
  if v_old != :doctors.consult_fee then
    insert into audit_log (table_name, row_key, action, details)
    values ('DOCTORS', :doctors.doctor_id, 'UPDATE',
            'consult_fee ' || v_old || ' -> ' || :doctors.consult_fee);
  end if;
end;
