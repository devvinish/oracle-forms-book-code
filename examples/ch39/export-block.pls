-- @where Program unit: procedure EXPORT_BLOCK (form CH39_FIND)
procedure export_block(p_block varchar2, p_file varchar2) is
  v_out   text_io.file_type;
  v_item  varchar2(100);
  v_line  varchar2(4000);
  v_n     pls_integer := 0;
  -- the displayed items of the block, other than buttons, in the order of the Object Navigator
  function is_column(p_item varchar2) return boolean is
  begin
    return get_item_property(p_item, ITEM_TYPE) <> 'BUTTON'
       and get_item_property(p_item, VISIBLE) = 'TRUE';
  end;
  function next_column(p_item varchar2) return varchar2 is   -- item names without the block
    v varchar2(100) := p_item;
  begin
    loop
      v := get_item_property(p_block || '.' || v, NEXTITEM);   -- qualified: another block may
      exit when v is null or is_column(p_block || '.' || v);   -- have an item of the same name
    end loop;
    return v;
  end;
begin
  v_out := text_io.fopen(p_file, 'w');            -- a file on the Forms server
  v_item := get_block_property(p_block, FIRST_ITEM);
  if not is_column(p_block || '.' || v_item) then
    v_item := next_column(v_item);
  end if;
  -- the header: the item names
  declare v varchar2(100) := v_item; begin
    while v is not null loop
      v_line := v_line || case when v_line is not null then ',' end || v;
      v := next_column(v);
    end loop;
  end;
  text_io.put_line(v_out, v_line);
  -- the records: every record of the block, fetched to the last
  go_block(p_block);
  first_record;
  loop
    v_line := null;
    declare v varchar2(100) := v_item; begin
      while v is not null loop
        v_line := v_line || case when v_line is not null then ',' end
                  || '"' || replace(name_in(p_block || '.' || v), '"', '""') || '"';
        v := next_column(v);
      end loop;
    end;
    text_io.put_line(v_out, v_line);
    v_n := v_n + 1;
    exit when :system.last_record = 'TRUE';
    next_record;
  end loop;
  text_io.fclose(v_out);
  first_record;
  message(v_n || ' records written to ' || p_file);
exception
  when others then
    if text_io.is_open(v_out) then
      text_io.fclose(v_out);
    end if;
    raise;
end;
