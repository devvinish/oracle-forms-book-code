-- @where SQL*Plus, as SYSTEM in the application's database (FORMSPDB in the lab)
-- first run frmsec.sql, from ORACLE_HOME/tools/dbtab/forms of the Forms installation
grant select on frm50_enabled_roles to public;
create role cw_user_role;                        -- every user of the menu
create role cw_fees_role;                        -- those who may change doctors' fees
grant cw_user_role to carewell;
