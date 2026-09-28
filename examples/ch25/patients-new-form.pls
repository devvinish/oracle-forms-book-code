-- @where Trigger: WHEN-NEW-FORM-INSTANCE (form CH25_PATIENTS)
begin
  cw_sec.login(:parameter.p_user);
  cw_sec.apply_menu;
  set_window_property('MAIN_WIN', title,
    'Patients of Pune - ' || cw_sec.full_name || ' (' || cw_sec.app_role || ')');
  if not cw_sec.has_role('ADMIN,RECEPTION') then
    set_block_read_only('PATIENTS', true);             -- doctors and others only look
  end if;
  go_block('PATIENTS');
  execute_query;
end;
