-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.EDIT
declare
  v_editing boolean := get_item_property('CTL.EDIT', label) = 'Edit';
begin
  set_block_read_only('PATIENTS', not v_editing);
  set_item_property('CTL.EDIT', label, case when v_editing then 'Lock' else 'Edit' end);
  go_block('PATIENTS');
end;
