-- @where Trigger: ON-ERROR (form CH27_FEE_PROC)
declare
  v_msg varchar2(400) := substr(dbms_error_text, 12);   -- after 'ORA-20010: '
begin
  if error_code in (40735, 40508, 40509, 40510)
     and dbms_error_code between -20999 and -20000 then  -- raise_application_error
    if instr(v_msg, 'ORA-') > 0 then                     -- drop the ORA-06512 lines
      v_msg := rtrim(substr(v_msg, 1, instr(v_msg, 'ORA-') - 1), chr(10) || ' ');
    end if;
    message(v_msg);
    raise form_trigger_failure;
  else
    cw_err.on_error;                                    -- the rest: Chapter 26
  end if;
end;
