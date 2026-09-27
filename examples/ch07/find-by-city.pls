-- @where Trigger: WHEN-BUTTON-PRESSED on FILTER.FIND
if :filter.city is null then
  set_block_property('PATIENTS', default_where, '');
else
  set_block_property('PATIENTS', default_where, 'city = :filter.city');
end if;
go_block('PATIENTS');
execute_query;
:filter.last_query := get_block_property('PATIENTS', last_query);
