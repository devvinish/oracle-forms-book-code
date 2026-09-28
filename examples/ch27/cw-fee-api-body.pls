-- @where Database: package body CW_FEE_API, in setup/carewell/code.sql
create or replace package body cw_fee_api as
  procedure query_fees(p_fees in out fee_cur, p_dept_id in number) is
  begin
    open p_fees for
      select doctor_id, first_name, last_name, consult_fee
      from   doctors
      where  dept_id = p_dept_id
      order  by last_name;
  end query_fees;

  procedure lock_fees(p_fees in out fee_tab) is
    v_id doctors.doctor_id%type;
  begin
    for i in 1 .. p_fees.count loop
      select doctor_id into v_id from doctors
      where  doctor_id = p_fees(i).doctor_id for update nowait;
    end loop;
  end lock_fees;

  procedure update_fees(p_fees in out fee_tab) is
    v_old doctors.consult_fee%type;
  begin
    for i in 1 .. p_fees.count loop
      if p_fees(i).consult_fee not between 50 and 500 then
        raise_application_error(-20010, 'Fees are between 50 and 500.');
      end if;
      select consult_fee into v_old from doctors where doctor_id = p_fees(i).doctor_id;
      update doctors set consult_fee = p_fees(i).consult_fee
      where  doctor_id = p_fees(i).doctor_id;
      insert into audit_log (table_name, row_key, action, details)
      values ('DOCTORS', p_fees(i).doctor_id, 'UPDATE',
              'consult_fee ' || v_old || ' -> ' || p_fees(i).consult_fee);
    end loop;
  end update_fees;
end cw_fee_api;
