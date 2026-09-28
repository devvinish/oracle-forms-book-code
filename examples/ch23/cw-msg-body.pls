-- @where Library CW_LIB: package CW_MSG (Package Body)
package body cw_msg is
  function ask(p_text varchar2, p_buttons varchar2 default 'OK',
               p_style varchar2 default 'NOTE') return pls_integer is
    v_alert varchar2(30) := 'CW_' || upper(p_style);   -- CW_NOTE, CW_CAUTION, CW_STOP
    v_rest  varchar2(100) := p_buttons || ',';
    v_btn   number;
  begin
    if id_null(find_alert(v_alert)) then
      message('CW_MSG: the form has no alert ' || v_alert);
      raise form_trigger_failure;
    end if;
    set_alert_property(v_alert, alert_message_text, p_text);
    for i in 1 .. 3 loop                              -- labels from 'Yes,No'
      exit when v_rest is null;
      set_alert_button_property(v_alert,
        case i when 1 then alert_button1 when 2 then alert_button2 else alert_button3 end,
        label, substr(v_rest, 1, instr(v_rest, ',') - 1));
      v_rest := substr(v_rest, instr(v_rest, ',') + 1);
    end loop;
    v_btn := show_alert(v_alert);
    return case v_btn when alert_button1 then 1 when alert_button2 then 2 else 3 end;
  end ask;

  procedure inform(p_text varchar2) is
    n pls_integer;
  begin
    n := ask(p_text);
  end inform;

  procedure fail(p_text varchar2) is
    n pls_integer;
  begin
    n := ask(p_text, 'OK', 'STOP');
    raise form_trigger_failure;
  end fail;
end cw_msg;
