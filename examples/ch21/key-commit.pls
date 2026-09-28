-- @where Trigger: KEY-COMMIT on the form
begin
  commit_form;
  if :system.form_status = 'QUERY' then        -- everything was saved
    go_block('AUDIT_LOG');
    execute_query;                             -- show the new audit rows
    go_block('DOCTORS');
  end if;
end;
