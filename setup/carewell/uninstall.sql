-- Removes the CareWell Clinic objects (run as CAREWELL).
begin
  for p in (select object_name from user_objects where object_type = 'PACKAGE' and object_name like 'CW\_%' escape '\') loop
    execute immediate 'drop package ' || p.object_name;
  end loop;
end;
/
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
