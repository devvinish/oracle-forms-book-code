-- @where Trigger: WHEN-TREE-NODE-SELECTED on NAV.TREE
declare
  v_value varchar2(100);
begin
  if :system.trigger_node_selected = 'TRUE' then
    v_value := ftree.get_tree_node_property('NAV.TREE', :system.trigger_node,
                                            ftree.node_value);
    -- a medicine: that medicine; a category: its medicines and its subcategories'
    if substr(v_value, 1, 1) = 'M' then
      set_block_property('MEDICINES', onetime_where,
                         'medicine_id = ' || substr(v_value, 2));
    else
      set_block_property('MEDICINES', onetime_where,
        'category_id in (select category_id from medicine_categories ' ||
        'start with category_id = ' || substr(v_value, 2) ||
        ' connect by prior category_id = parent_id)');
    end if;
    go_block('MEDICINES');
    execute_query;
  end if;
end;
