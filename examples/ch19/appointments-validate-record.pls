-- @where Trigger: WHEN-VALIDATE-RECORD on APPOINTMENTS
declare
  v_clash appointments.appt_id%type;
begin
  select min(appt_id)
  into   v_clash
  from   appointments
  where  doctor_id = :appointments.doctor_id
  and    appt_id  != nvl(:appointments.appt_id, -1)
  and    status in ('BOOKED', 'CHECKED_IN')
  and    appt_start < :appointments.appt_start + :appointments.duration_min / 1440
  and    appt_start + duration_min / 1440 > :appointments.appt_start;

  if v_clash is not null then
    message('Doctor ' || :appointments.doctor_id || ' already has appointment ' || v_clash ||
            ' at this time.');
    raise form_trigger_failure;
  end if;
end;
