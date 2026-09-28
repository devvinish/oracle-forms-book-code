-- @where Database: package CW_FEE_API, in setup/carewell/code.sql
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
