-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.REACTIVATE (form CH39_DOCTORS)
if :doctors.active = 'N' then
  :doctors.active := 'Y';
  commit_form;
else
  message('Dr ' || :doctors.last_name || ' is active.');
end if;
