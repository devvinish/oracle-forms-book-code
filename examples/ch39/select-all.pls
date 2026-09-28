-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.SELECT_ALL (form CH39_DAY)
go_block('APPOINTMENTS');
first_record;
:ctl.selected := 0;
loop
  exit when :appointments.appt_id is null;           -- an empty block
  :appointments.sel := 'Y';
  :ctl.selected := :ctl.selected + 1;
  exit when :system.last_record = 'TRUE';
  next_record;
end loop;
first_record;
