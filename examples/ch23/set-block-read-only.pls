-- @where Library CW_LIB: procedure SET_BLOCK_READ_ONLY
procedure set_block_read_only(p_block varchar2, p_read_only boolean) is
  v_item  varchar2(61) := get_block_property(p_block, first_item);
  v_name  varchar2(61);
  v_value number := case when p_read_only then property_false else property_true end;
begin
  while v_item is not null loop
    v_name := p_block || '.' || v_item;
    if get_item_property(v_name, item_type) in ('TEXT ITEM', 'LIST', 'RADIO GROUP')
       and get_item_property(v_name, base_table) = 'TRUE'
       and get_item_property(v_name, item_canvas) is not null then
      set_item_property(v_name, update_allowed, v_value);
      set_item_property(v_name, insert_allowed, v_value);
    end if;
    v_item := get_item_property(v_name, nextitem);
  end loop;
  set_block_property(p_block, delete_allowed, v_value);
end;
