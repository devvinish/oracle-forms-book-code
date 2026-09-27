-- @where Trigger: WHEN-VALIDATE-ITEM on PATIENTS.BIRTH_DATE
if :patients.birth_date > trunc(sysdate) then
  message('The birth date cannot be in the future.');
  raise form_trigger_failure;
end if;
:patients.age := age_in_years(:patients.birth_date);
