-- CareWell Clinic: stored program units that the forms of the book call (Chapter 17 and later).
-- Run as CAREWELL; install.sql runs it after schema.sql and data.sql.

create or replace package cw_api as
  -- a one-line summary of a patient's visits: how many, the last one, and the doctors seen
  function patient_summary(p_patient_id in patients.patient_id%type) return varchar2;

  -- everything a list of appointments shows about one appointment, in one call (Chapter 34)
  procedure appt_details(p_appt_id in  appointments.appt_id%type,
                         p_patient out varchar2,
                         p_doctor  out varchar2,
                         p_billed  out number);
end cw_api;
/

create or replace package body cw_api as
  function patient_summary(p_patient_id in patients.patient_id%type) return varchar2 is
    v_count   pls_integer;
    v_last    date;
    v_doctors varchar2(400);
  begin
    select count(*), max(v.visit_date)
    into   v_count, v_last
    from   visits v
    where  v.patient_id = p_patient_id;

    select listagg(distinct d.last_name, ', ') within group (order by d.last_name)
    into   v_doctors
    from   visits v
           join doctors d on d.doctor_id = v.doctor_id
    where  v.patient_id = p_patient_id;

    return case when v_count = 0 then 'No visits'
                else v_count || ' visits, last on ' || to_char(v_last, 'DD-MON-YYYY')
                     || '; doctors: ' || v_doctors end;
  end patient_summary;

  procedure appt_details(p_appt_id in  appointments.appt_id%type,
                         p_patient out varchar2,
                         p_doctor  out varchar2,
                         p_billed  out number) is
  begin
    select p.first_name || ' ' || p.last_name, 'Dr. ' || d.last_name,
           (select max(i.total_amount)
            from   visits v join invoices i on i.visit_id = v.visit_id
            where  v.appt_id = a.appt_id)
    into   p_patient, p_doctor, p_billed
    from   appointments a
           join patients p on p.patient_id = a.patient_id
           join doctors d  on d.doctor_id  = a.doctor_id
    where  a.appt_id = p_appt_id;
  end appt_details;
end cw_api;
/

create or replace package cw_fee_api as
  -- the fees of a department's doctors, for a block based on procedures (Chapter 27)
  type fee_rec is record (
    doctor_id   doctors.doctor_id%type,
    first_name  doctors.first_name%type,
    last_name   doctors.last_name%type,
    consult_fee doctors.consult_fee%type);
  type fee_cur is ref cursor return fee_rec;
  type fee_tab is table of fee_rec index by binary_integer;

  procedure query_fees(p_fees in out fee_cur, p_dept_id in number);
  procedure lock_fees(p_fees in out fee_tab);
  procedure update_fees(p_fees in out fee_tab);
end cw_fee_api;
/

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
/
