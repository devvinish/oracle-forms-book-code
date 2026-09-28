-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.CLEAR_NOTES
declare
  v_button number;
begin
  if :visits.notes is null then
    v_button := show_alert('AL_NO_NOTES');           -- a note: one OK button
  elsif show_alert('AL_CLEAR_NOTES') = alert_button1 then
    :visits.notes := null;
  end if;
end;
