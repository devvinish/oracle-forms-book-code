-- @where Trigger: WHEN-CHECKBOX-CHANGED on CTL.READ_ONLY
declare
  v_ro boolean := checkbox_checked('CTL.READ_ONLY');
begin
  set_block_read_only('PATIENTS', v_ro);
  set_item_property('PATIENTS.LAST_NAME', prompt_text,
    case when v_ro then 'Last Name (read only)' else 'Last Name' end);
  set_radio_button_property('PATIENTS.GENDER', 'OTHER', enabled,
    case when v_ro then property_false else property_true end);
end;
