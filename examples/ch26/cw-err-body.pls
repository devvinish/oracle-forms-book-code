-- @where Library CW_LIB: package CW_ERR (Package Body)
package body cw_err is
  function constraint_of(p_text varchar2) return varchar2 is
  begin
    return regexp_substr(p_text, '\(\w+\.(\w+)\)', 1, 1, null, 1);
  end constraint_of;

  procedure on_error is
    v_db   number := dbms_error_code;                -- the database error, or 0
    v_name varchar2(128) := constraint_of(dbms_error_text);
    v_text varchar2(400);
  begin
    if error_type = 'FRM' and error_code in (40508, 40509, 40510) then
      v_text := case
        when v_db = -1    then 'This record already exists.'
        when v_db = -1400 then                     -- cannot insert NULL into (...."COLUMN")
          'Enter a value for '
          || regexp_substr(dbms_error_text, '"(\w+)"\)', 1, 1, null, 1) || '.'
        when v_name = 'APPOINTMENTS_PATIENT_FK' then 'There is no patient with this number.'
        when v_name = 'APPOINTMENTS_DOCTOR_FK' then 'There is no doctor with this number.'
        when v_name = 'APPOINTMENTS_DUR_CK' then 'An appointment lasts 5 to 240 minutes.'
        when v_db = -2292 then 'Other records still refer to this one.'
      end;
    end if;
    if v_text is null then                           -- no translation: Forms' own message
      v_text := error_type || '-' || to_char(error_code) || ': ' || error_text;
    end if;
    message(v_text);
    raise form_trigger_failure;
  end on_error;
end cw_err;
