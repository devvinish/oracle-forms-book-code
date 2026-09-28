-- @where Program unit: procedure SORT_BY (form CH39_FIND)
procedure sort_by(p_column varchar2, p_heading varchar2, p_label varchar2) is
begin
  if :ctl.sort_column = p_column and :ctl.sort_dir = 'ASC' then
    :ctl.sort_dir := 'DESC';                -- a second click turns the order around
  else
    :ctl.sort_dir := 'ASC';
  end if;
  -- the previous heading loses its arrow, the new one gets it
  if :ctl.sort_heading is not null then
    set_item_property(:ctl.sort_heading, LABEL, :ctl.sort_label);
  end if;
  :ctl.sort_column  := p_column;
  :ctl.sort_heading := p_heading;
  :ctl.sort_label   := p_label;
  set_item_property(p_heading, LABEL,                 -- an up or down triangle after the label
                    p_label || ' ' || case :ctl.sort_dir when 'ASC' then unistr('\25B2') else unistr('\25BC') end);
  set_block_property('PATIENTS', ORDER_BY, p_column || ' ' || :ctl.sort_dir);
  go_block('PATIENTS');
  execute_query;
end;
