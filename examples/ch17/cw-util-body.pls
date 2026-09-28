-- @where Program unit: CW_UTIL (Package Body)
package body cw_util is
  function age_in_years(p_birth_date date) return number is
  begin
    return trunc(months_between(sysdate, p_birth_date) / 12);
  end age_in_years;
end cw_util;
