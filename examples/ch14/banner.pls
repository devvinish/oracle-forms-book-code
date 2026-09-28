-- @where Trigger: WHEN-NEW-FORM-INSTANCE on the form
begin
  set_item_property('CTL.BANNER', background_color, 'r40g86b176');   -- 0-255 values
  set_item_property('CTL.BANNER', foreground_color, 'r255g255b255');
  :ctl.banner := '  Dr. Sara Nair - Cardiology';
  go_block('APPOINTMENTS');
  execute_query;
end;
