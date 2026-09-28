-- @where Program unit: procedure CHECK_DOUBLE_BOOKING (form CH39_BOOKING)
-- one doctor, one patient at a time: refuses an appointment that overlaps another of the same doctor
procedure check_double_booking is
  v_other appointments.appt_id%type;
begin
  if :appointments.status = 'CANCELLED' then
    return;
  end if;
  select min(appt_id) into v_other
    from appointments a
   where a.doctor_id = :appointments.doctor_id
     and a.status <> 'CANCELLED'
     and a.appt_id <> nvl(:appointments.appt_id, -1)
     and a.appt_start < :appointments.appt_start + :appointments.duration_min / 1440
     and :appointments.appt_start < a.appt_start + a.duration_min / 1440;
  if v_other is not null then
    message('Dr ' || :appointments.doctor_name || ' already has appointment ' || v_other
            || ' at that time.');
    raise form_trigger_failure;
  end if;
end;
