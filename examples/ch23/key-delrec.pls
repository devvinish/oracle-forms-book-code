-- @where Trigger: KEY-DELREC on block PATIENTS
if cw_msg.ask('Delete ' || :patients.first_name || ' ' || :patients.last_name
              || ' and every record of this patient?', 'Delete,Keep', 'CAUTION') = 1 then
  delete_record;
end if;
