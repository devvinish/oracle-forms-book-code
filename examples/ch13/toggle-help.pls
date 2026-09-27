-- @where Trigger: WHEN-BUTTON-PRESSED on TOOLS.HELP
if get_view_property('HELP_STK', visible) = 'TRUE' then
  hide_view('HELP_STK');
else
  show_view('HELP_STK');
end if;
