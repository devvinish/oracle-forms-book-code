-- @where Trigger: WHEN-TIMER-EXPIRED (form CH29_WAITING_ROOM)
declare
  v_timer varchar2(30) := get_application_property(timer_name);
begin
  if v_timer = 'CLOCK' then
    :ctl.now := to_char(sysdate, 'HH24:MI:SS');
  elsif v_timer = 'FIND' then                        -- one-shot: see WHEN-VALIDATE-ITEM
    go_block('APPOINTMENTS');
    first_record;
    loop
      exit when upper(:appointments.patient) like upper(:ctl.find) || '%'
             or :system.last_record = 'TRUE';
      next_record;
    end loop;
  end if;
end;
