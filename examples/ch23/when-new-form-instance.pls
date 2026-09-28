-- @where Trigger: WHEN-NEW-FORM-INSTANCE (form level)
go_block('PATIENTS');
execute_query;
set_block_read_only('PATIENTS', true);          -- from CW_LIB
