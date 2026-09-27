-- @where Trigger: WHEN-WINDOW-CLOSED on the form
if :system.event_window = 'ALLERGY_WIN' then
  go_item('PATIENTS.MRN');                -- leave the dialog's item first
  hide_window('ALLERGY_WIN');
else
  exit_form;
end if;
