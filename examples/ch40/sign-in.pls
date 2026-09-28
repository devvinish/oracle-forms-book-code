-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.SIGN_IN (form CW_LOGIN)
cw_sec.login(:ctl.username);                    -- fails with a message for an unknown user
new_form('cw_main', full_rollback, no_query_only, share_library_data);
