-- @where Trigger: WHEN-CHECKBOX-CHANGED on DOCTORS.ACTIVE
if not checkbox_checked('DOCTORS.ACTIVE') then
  message('Dr. ' || :doctors.last_name || ' will no longer be offered for new appointments.');
end if;
