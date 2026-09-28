-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.REMIND (form CH39_DAY)
declare
  v_out   text_io.file_type;
  v_total pls_integer;
  v_done  pls_integer := 0;
begin
  select count(*) into v_total
    from appointments where status = 'BOOKED' and appt_start > sysdate;
  v_out := text_io.fopen('/work/transfer/out/reminders.txt', 'w');
  set_application_property(CURSOR_STYLE, 'BUSY');
  for r in (select a.appt_start, p.first_name, p.phone, d.last_name doctor
              from appointments a, patients p, doctors d
             where p.patient_id = a.patient_id and d.doctor_id = a.doctor_id
               and a.status = 'BOOKED' and a.appt_start > sysdate
             order by a.appt_start) loop
    text_io.put_line(v_out, r.phone || ': Dear ' || r.first_name || ', a reminder of your appointment with Dr '
                            || r.doctor || ' on ' || to_char(r.appt_start, 'DD-MON-YYYY "at" HH24:MI') || '.');
    dbms_session.sleep(0.02);           -- the lab's pause, so that the bar can be watched
    v_done := v_done + 1;
    if mod(v_done, 10) = 0 or v_done = v_total then
      :ctl.progress := round(100 * v_done / v_total);
      synchronize;                      -- show the new value now, not when the trigger ends
    end if;
  end loop;
  text_io.fclose(v_out);
  set_application_property(CURSOR_STYLE, 'DEFAULT');
  message(v_done || ' reminders written to /work/transfer/out/reminders.txt');
end;
