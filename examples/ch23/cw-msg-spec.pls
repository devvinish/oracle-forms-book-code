-- @where Library CW_LIB: package CW_MSG (Package Spec)
package cw_msg is
  -- shows a message box and returns the button pressed: 1, 2, or 3
  function ask(p_text varchar2, p_buttons varchar2 default 'OK',
               p_style varchar2 default 'NOTE') return pls_integer;
  procedure inform(p_text varchar2);
  procedure fail(p_text varchar2);        -- stop alert, then FORM_TRIGGER_FAILURE
end cw_msg;
