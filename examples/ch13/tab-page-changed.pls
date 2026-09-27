-- @where Trigger: WHEN-TAB-PAGE-CHANGED on the form
if :system.tab_new_page = 'APPTS' then
  go_block('APPOINTMENTS');
elsif :system.tab_new_page = 'VISITS' then
  go_block('VISITS');
else
  go_item('PATIENTS.BIRTH_DATE');
end if;
