-- @where Trigger: WHEN-VALIDATE-ITEM on PATIENTS.PHONE
if not regexp_like(:patients.phone, '^\+91 [6-9][0-9]{9}$') then
  cw_msg.fail('Enter the phone as +91, a space, and ten digits: +91 9880200017.');
end if;
