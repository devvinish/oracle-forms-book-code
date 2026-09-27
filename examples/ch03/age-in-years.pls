-- @where Program unit: AGE_IN_YEARS
function age_in_years (p_birth_date date) return number is
begin
  return trunc(months_between(sysdate, p_birth_date) / 12);
end;
