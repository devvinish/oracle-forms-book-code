-- @where Trigger: ON-MESSAGE (form level)
if message_code = 40400 then        -- FRM-40400: Transaction complete: ... saved.
  message('Saved.');
else
  message(message_type || '-' || to_char(message_code) || ': ' || message_text);
end if;
