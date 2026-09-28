-- @where Program unit: procedure FIND_PATIENTS (form CH39_FIND)
procedure find_patients is
  v_where varchar2(1000);
begin
  -- each criterion the user filled adds a condition; the values stay bind references
  if :ctl.name is not null then
    v_where := v_where || ' and upper(last_name || '' '' || first_name) like ''%'' || upper(:ctl.name) || ''%''';
  end if;
  if :ctl.city is not null then
    v_where := v_where || ' and city = :ctl.city';
  end if;
  if :ctl.born_from is not null then
    v_where := v_where || ' and birth_date >= :ctl.born_from';
  end if;
  if :ctl.born_to is not null then
    v_where := v_where || ' and birth_date < :ctl.born_to + 1';
  end if;
  set_block_property('PATIENTS', DEFAULT_WHERE, substr(v_where, 6));   -- without the first ' and '
  go_block('PATIENTS');
  :system.message_level := '25';         -- hide FRM-40355, the message of COUNT_QUERY (level 25)
  count_query;
  :system.message_level := '0';
  :ctl.total := get_block_property('PATIENTS', QUERY_HITS);
  execute_query;
end;
