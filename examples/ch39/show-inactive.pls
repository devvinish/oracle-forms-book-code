-- @where Trigger: WHEN-CHECKBOX-CHANGED on CTL.SHOW_INACTIVE (form CH39_DOCTORS)
-- (setting DEFAULT_WHERE to null left the block's WHERE clause in place: give a condition instead)
set_block_property('DOCTORS', DEFAULT_WHERE,
                   case :ctl.show_inactive when 'Y' then 'active in (''Y'', ''N'')' else 'active = ''Y''' end);
go_block('DOCTORS');
execute_query;
