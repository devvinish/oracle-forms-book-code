-- @where Menu CW_MENU: item FEES of menu CLINIC (Menu Item Code)
if id_null(find_form('CH21_FEES')) then
  open_form('ch21_fees');                    -- not open yet
else
  go_form('CH21_FEES');                      -- already open: go to it
end if;
