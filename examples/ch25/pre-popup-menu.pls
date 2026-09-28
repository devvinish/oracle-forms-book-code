-- @where Trigger: PRE-POPUP-MENU (block PATIENTS)
set_menu_item_property('POP_PATIENT.VISITS', enabled,
  case when cw_sec.has_role('ADMIN,DOCTOR') then property_true else property_false end);
