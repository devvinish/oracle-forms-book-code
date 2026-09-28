-- @where Trigger: WHEN-LIST-CHANGED on APPOINTMENTS.DEPT_ID (form CH39_BOOKING)
-- a doctor of another department no longer fits: clear the doctor
if :appointments.doctor_id is not null then
  declare
    v_dept doctors.dept_id%type;
  begin
    select dept_id into v_dept from doctors where doctor_id = :appointments.doctor_id;
    if v_dept <> :appointments.dept_id then
      :appointments.doctor_id   := null;
      :appointments.doctor_name := null;
    end if;
  end;
end if;
