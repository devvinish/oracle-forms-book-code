-- Removes the CareWell Clinic objects (run as CAREWELL).
begin
  for t in (select table_name from user_tables where table_name <> 'AUDIT_LOG') loop
    execute immediate 'drop table ' || t.table_name || ' cascade constraints purge';
  end loop;
end;
/
drop table audit_log purge;
drop view invoice_totals;
begin
  for s in (select sequence_name from user_sequences where sequence_name like '%\_SEQ' escape '\') loop
    execute immediate 'drop sequence ' || s.sequence_name;
  end loop;
end;
/
