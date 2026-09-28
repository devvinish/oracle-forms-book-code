-- @where Trigger: WHEN-NEW-RECORD-INSTANCE on block PATIENTS (form CH39_FIND)
if :patients.patient_id is null then
  :ctl.counter := null;
else
  :ctl.counter := 'Patient ' || :system.cursor_record || ' of ' || :ctl.total;
end if;
