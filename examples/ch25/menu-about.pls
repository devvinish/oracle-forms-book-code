-- @where Menu CW_MENU: item ABOUT of menu HELP (Menu Item Code)
message('Signed in as ' || :global.cw_user || '. ' || :system.cursor_item
        || ' = ' || name_in(:system.cursor_item));
