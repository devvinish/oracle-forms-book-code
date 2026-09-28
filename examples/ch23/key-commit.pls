-- @where Trigger: KEY-COMMIT (form level)
commit_form;
if :system.form_status = 'QUERY' then
  cw_msg.inform('Your changes are saved.');
end if;
