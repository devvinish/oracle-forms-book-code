-- CareWell Clinic: stored program units that the forms of the book call (Chapter 17 and later).
-- Run as CAREWELL; install.sql runs it after schema.sql and data.sql.

create or replace package cw_api as
  -- a one-line summary of a patient's visits: how many, the last one, and the doctors seen
  function patient_summary(p_patient_id in patients.patient_id%type) return varchar2;
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
end cw_api;
/
